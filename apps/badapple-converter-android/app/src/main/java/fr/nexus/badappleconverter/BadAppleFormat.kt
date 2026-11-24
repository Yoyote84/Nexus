package fr.nexus.badappleconverter

import java.io.ByteArrayOutputStream
import java.io.OutputStream

/** Binary RLE container used by the reference Cardputer ADV Bad Apple player. */
internal object BadAppleFormat {
    const val WIDTH = 240
    const val HEIGHT = 135
    const val FPS = 8
    const val RAW_FRAME_BYTES = WIDTH * HEIGHT / 8

    // AV_PIX_FMT_MONOBLACK: 0 is black, 1 is white, pixels MSB-first.
    fun packMonochrome(argbPixels: IntArray, threshold: Int): ByteArray {
        require(argbPixels.size == WIDTH * HEIGHT) { "La trame doit faire 240 × 135 pixels." }
        require(threshold in 0..255) { "Seuil hors plage." }
        val packed = ByteArray(RAW_FRAME_BYTES)
        for (byteIndex in packed.indices) {
            var value = 0
            val firstPixel = byteIndex * 8
            for (bit in 0..7) {
                val color = argbPixels[firstPixel + bit]
                val red = (color shr 16) and 0xFF
                val green = (color shr 8) and 0xFF
                val blue = color and 0xFF
                val luminance = (299 * red + 587 * green + 114 * blue) / 1000
                if (luminance >= threshold) value = value or (1 shl (7 - bit))
            }
            packed[byteIndex] = value.toByte()
        }
        return packed
    }

    // 01..7F: N black bytes; 81..FF: N white bytes; 00 value: literal; 80: frame end.
    fun encodeFrame(raw: ByteArray): ByteArray {
        val encoded = ByteArrayOutputStream(raw.size / 2 + 16)
        var index = 0
        while (index < raw.size) {
            val value = raw[index].toInt() and 0xFF
            if (value == 0x00 || value == 0xFF) {
                var count = 1
                while (
                    index + count < raw.size &&
                    count < 127 &&
                    (raw[index + count].toInt() and 0xFF) == value
                ) count++
                encoded.write(if (value == 0x00) count else (0x80 or count))
                index += count
            } else {
                encoded.write(0x00)
                encoded.write(value)
                index++
            }
        }
        encoded.write(0x80)
        return encoded.toByteArray()
    }

    fun writeContainerHeader(output: OutputStream, frameCount: Int, offsets: List<Long>) {
        require(frameCount > 0 && offsets.size == frameCount) { "En-tête d'index invalide." }
        writeUInt32LE(output, frameCount.toLong())
        offsets.forEach { writeUInt32LE(output, it) }
    }

    fun writeUInt32LE(output: OutputStream, value: Long) {
        require(value in 0L..0xFFFF_FFFFL) { "Valeur hors plage uint32." }
        output.write((value and 0xFF).toInt())
        output.write(((value shr 8) and 0xFF).toInt())
        output.write(((value shr 16) and 0xFF).toInt())
        output.write(((value shr 24) and 0xFF).toInt())
    }

    internal fun decodeFrame(encoded: ByteArray, expectedSize: Int): ByteArray {
        val decoded = ByteArrayOutputStream(expectedSize)
        var index = 0
        while (index < encoded.size && decoded.size() < expectedSize) {
            val code = encoded[index++].toInt() and 0xFF
            when {
                code == 0x80 -> break
                code == 0x00 -> {
                    require(index < encoded.size) { "Octet littéral manquant." }
                    decoded.write(encoded[index++].toInt() and 0xFF)
                }
                code < 0x80 -> repeat(code) { decoded.write(0x00) }
                else -> repeat(code and 0x7F) { decoded.write(0xFF) }
            }
            require(decoded.size() <= expectedSize) { "Trame RLE trop longue." }
        }
        require(decoded.size() == expectedSize) { "Trame RLE incomplète." }
        return decoded.toByteArray()
    }
}
