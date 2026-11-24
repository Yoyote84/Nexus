package fr.nexus.badappleconverter

import android.content.Context
import android.graphics.Bitmap
import android.media.MediaMetadataRetriever
import android.net.Uri
import java.io.BufferedInputStream
import java.io.File
import java.io.FileInputStream
import java.io.FileOutputStream
import java.io.IOException
import kotlin.math.ceil

internal object BadAppleConverter {
    data class Result(val frameCount: Int, val durationMs: Long, val outputBytes: Long)

    fun convert(
        context: Context,
        source: Uri,
        destination: Uri,
        threshold: Int,
        onProgress: (completed: Int, total: Int) -> Unit
    ): Result {
        val retriever = MediaMetadataRetriever()
        val payloadFile = File.createTempFile("nexus-badapple-", ".frames", context.cacheDir)
        try {
            retriever.setDataSource(context, source)
            val durationMs = retriever
                .extractMetadata(MediaMetadataRetriever.METADATA_KEY_DURATION)
                ?.toLongOrNull()
                ?.takeIf { it > 0L }
                ?: throw IOException("Durée vidéo introuvable ou vidéo illisible.")

            val frameCountLong = ceil(durationMs.toDouble() * BadAppleFormat.FPS / 1000.0).toLong()
            if (frameCountLong !in 1L..200_000L) {
                throw IOException("Vidéo trop longue : limite fixée à 200 000 images.")
            }
            val frameCount = frameCountLong.toInt()
            val offsets = ArrayList<Long>(frameCount)
            var payloadSize = 0L

            FileOutputStream(payloadFile).buffered().use { payload ->
                for (frameIndex in 0 until frameCount) {
                    val timestampMs = (frameIndex.toLong() * 1000L / BadAppleFormat.FPS)
                        .coerceAtMost(durationMs - 1L)
                    val bitmap = retriever.getFrameAtTime(
                        timestampMs * 1000L,
                        MediaMetadataRetriever.OPTION_CLOSEST
                    ) ?: throw IOException("Impossible de décoder l'image no ${frameIndex + 1}.")

                    val scaled = if (
                        bitmap.width == BadAppleFormat.WIDTH &&
                        bitmap.height == BadAppleFormat.HEIGHT
                    ) bitmap else Bitmap.createScaledBitmap(
                        bitmap, BadAppleFormat.WIDTH, BadAppleFormat.HEIGHT, true
                    )
                    val pixels = IntArray(BadAppleFormat.WIDTH * BadAppleFormat.HEIGHT)
                    try {
                        scaled.getPixels(
                            pixels, 0, BadAppleFormat.WIDTH,
                            0, 0, BadAppleFormat.WIDTH, BadAppleFormat.HEIGHT
                        )
                    } finally {
                        if (scaled !== bitmap && !scaled.isRecycled) scaled.recycle()
                        if (!bitmap.isRecycled) bitmap.recycle()
                    }

                    val encoded = BadAppleFormat.encodeFrame(
                        BadAppleFormat.packMonochrome(pixels, threshold)
                    )
                    if (payloadSize > 0xFFFF_FFFFL - encoded.size.toLong()) {
                        throw IOException("Le fichier dépasse la limite de 4 Gio du format.")
                    }
                    offsets.add(payloadSize)
                    payload.write(encoded)
                    payloadSize += encoded.size
                    onProgress(frameIndex + 1, frameCount)
                }
            }

            val output = context.contentResolver.openOutputStream(destination, "wt")
                ?: throw IOException("Android n'a pas pu ouvrir le fichier de destination.")
            output.buffered().use { stream ->
                BadAppleFormat.writeContainerHeader(stream, frameCount, offsets)
                BufferedInputStream(FileInputStream(payloadFile)).use { input -> input.copyTo(stream) }
                stream.flush()
            }

            val headerBytes = 4L + frameCount.toLong() * 4L
            return Result(frameCount, durationMs, headerBytes + payloadSize)
        } finally {
            try { retriever.release() } catch (_: Exception) { }
            payloadFile.delete()
        }
    }
}
