package fr.nexus.badappleconverter

import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Test
import java.io.ByteArrayOutputStream

class BadAppleFormatTest {
    @Test
    fun rleRoundTripPreservesBlackWhiteAndLiteralBytes() {
        val raw = byteArrayOf(0x00, 0x00, 0x00, 0xFF.toByte(), 0xFF.toByte(), 0x12, 0x80.toByte(), 0x34)
        val encoded = BadAppleFormat.encodeFrame(raw)
        assertEquals(0x80, encoded.last().toInt() and 0xFF)
        assertArrayEquals(raw, BadAppleFormat.decodeFrame(encoded, raw.size))
    }

    @Test
    fun longRunsAreSplitAt127Bytes() {
        val raw = ByteArray(4050) { 0xFF.toByte() }
        val encoded = BadAppleFormat.encodeFrame(raw)
        assertArrayEquals(raw, BadAppleFormat.decodeFrame(encoded, raw.size))
        assertEquals(0x80, encoded.last().toInt() and 0xFF)
    }

    @Test
    fun monochromePackingUsesMostSignificantBitFirst() {
        val black = 0xFF000000.toInt()
        val white = 0xFFFFFFFF.toInt()
        val pixels = IntArray(240 * 135) { black }
        pixels[0] = white
        pixels[7] = white
        val packed = BadAppleFormat.packMonochrome(pixels, 128)
        assertEquals(0x81, packed[0].toInt() and 0xFF)
        assertEquals(0x00, packed[1].toInt() and 0xFF)
    }

    @Test
    fun containerHeaderIsLittleEndianAndOffsetsAreRelative() {
        val output = ByteArrayOutputStream()
        BadAppleFormat.writeContainerHeader(output, 2, listOf(0L, 123L))
        assertArrayEquals(
            byteArrayOf(2, 0, 0, 0, 0, 0, 0, 0, 123, 0, 0, 0),
            output.toByteArray()
        )
    }
}
