package fr.nexus.badappleconverter

import android.app.Activity
import android.content.Intent
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.net.Uri
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.Button
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.ScrollView
import android.widget.SeekBar
import android.widget.TextView
import java.util.concurrent.Executors

class MainActivity : Activity() {
    private val executor = Executors.newSingleThreadExecutor()
    private var selectedVideo: Uri? = null
    private lateinit var sourceLabel: TextView
    private lateinit var thresholdLabel: TextView
    private lateinit var progressBar: ProgressBar
    private lateinit var statusLabel: TextView
    private lateinit var chooseButton: Button
    private lateinit var convertButton: Button
    private var threshold = 128

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.statusBarColor = Color.rgb(11, 18, 32)
        window.navigationBarColor = Color.rgb(11, 18, 32)
        buildScreen()
    }

    private fun buildScreen() {
        val page = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(22), dp(24), dp(22), dp(24))
            setBackgroundColor(Color.rgb(11, 18, 32))
        }
        val scroll = ScrollView(this).apply {
            isFillViewport = true
            addView(page)
        }
        setContentView(scroll)

        page.addView(text("NEXUS  /  CARDPUTER ADV", 12, Color.rgb(142, 232, 209), true), matchWrap())
        page.addView(space(10))
        page.addView(text("BadApple", 32, Color.WHITE, true), matchWrap())
        page.addView(text("CONVERTISSEUR VIDÉO", 13, Color.rgb(180, 195, 214), true), matchWrap())
        page.addView(space(18))
        page.addView(text(
            "Transforme une vidéo de ton téléphone en fichier monochrome optimisé pour un lecteur Bad Apple du Cardputer ADV.",
            15, Color.rgb(220, 228, 239), false
        ), matchWrap())
        page.addView(space(22))

        val formatCard = card()
        formatCard.addView(text("FORMAT DE SORTIE", 12, Color.rgb(142, 232, 209), true))
        formatCard.addView(space(8))
        formatCard.addView(text("240 × 135 px   •   8 images/s   •   RLE", 16, Color.WHITE, true))
        formatCard.addView(text("Fichier attendu : /video/badapple.dat", 13, Color.rgb(180, 195, 214), false))
        page.addView(formatCard, matchWrap())
        page.addView(space(18))

        sourceLabel = text("Aucune vidéo sélectionnée", 14, Color.rgb(220, 228, 239), false)
        page.addView(sourceLabel, matchWrap())
        page.addView(space(10))

        chooseButton = button("CHOISIR UNE VIDÉO", true) {
            val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                addCategory(Intent.CATEGORY_OPENABLE)
                type = "video/*"
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION)
            }
            startActivityForResult(intent, REQUEST_VIDEO)
        }
        page.addView(chooseButton, matchWidth())

        page.addView(space(22))
        thresholdLabel = text("Seuil noir / blanc : 128", 14, Color.WHITE, true)
        page.addView(thresholdLabel, matchWrap())
        val thresholdSeek = SeekBar(this).apply {
            max = 255
            progress = threshold
            progressTintList = android.content.res.ColorStateList.valueOf(Color.rgb(142, 232, 209))
            thumbTintList = android.content.res.ColorStateList.valueOf(Color.rgb(142, 232, 209))
            setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
                override fun onProgressChanged(seekBar: SeekBar?, value: Int, fromUser: Boolean) {
                    threshold = value
                    thresholdLabel.text = "Seuil noir / blanc : $value"
                }
                override fun onStartTrackingTouch(seekBar: SeekBar?) = Unit
                override fun onStopTrackingTouch(seekBar: SeekBar?) = Unit
            })
        }
        page.addView(thresholdSeek, matchWidth())

        page.addView(space(22))
        convertButton = button("CRÉER badapple.dat", false) {
            if (selectedVideo == null) {
                setStatus("Sélectionne d'abord une vidéo.")
            } else {
                val intent = Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
                    addCategory(Intent.CATEGORY_OPENABLE)
                    type = "application/octet-stream"
                    putExtra(Intent.EXTRA_TITLE, "badapple.dat")
                }
                startActivityForResult(intent, REQUEST_OUTPUT)
            }
        }
        convertButton.isEnabled = false
        convertButton.alpha = 0.45f
        page.addView(convertButton, matchWidth())

        page.addView(space(18))
        progressBar = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
            max = 100
            progress = 0
            visibility = View.GONE
        }
        page.addView(progressBar, matchWidth())
        statusLabel = text("Conversion locale : aucune connexion Internet requise.", 13, Color.rgb(180, 195, 214), false)
        page.addView(statusLabel, matchWrap())
        page.addView(space(24))
        page.addView(text(
            "Après conversion, copie le fichier sur la carte microSD dans le dossier video, pour obtenir /video/badapple.dat.",
            13, Color.rgb(180, 195, 214), false
        ), matchWrap())
        page.addView(space(10))
        page.addView(text("Nexus • outil compagnon Android", 11, Color.rgb(104, 123, 148), false), matchWrap())
    }

    @Deprecated("Legacy result API avoids adding an unnecessary AndroidX dependency.")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode != RESULT_OK) return
        val uri = data?.data ?: return
        when (requestCode) {
            REQUEST_VIDEO -> {
                selectedVideo = uri
                try {
                    contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
                } catch (_: SecurityException) {
                    // A transient picker permission is enough for the current conversion.
                }
                sourceLabel.text = "Vidéo sélectionnée : ${uri.lastPathSegment ?: "fichier vidéo"}"
                convertButton.isEnabled = true
                convertButton.alpha = 1f
                setStatus("Prêt. Sortie en 240 × 135 à 8 images/s.")
            }
            REQUEST_OUTPUT -> startConversion(uri)
        }
    }

    private fun startConversion(destination: Uri) {
        val source = selectedVideo ?: return
        val selectedThreshold = threshold
        chooseButton.isEnabled = false
        convertButton.isEnabled = false
        progressBar.progress = 0
        progressBar.visibility = View.VISIBLE
        setStatus("Préparation de la vidéo…")

        executor.execute {
            try {
                val result = BadAppleConverter.convert(this, source, destination, selectedThreshold) { completed, total ->
                    runOnUiThread {
                        progressBar.progress = completed * 100 / total
                        statusLabel.text = "Conversion : $completed / $total images"
                    }
                }
                runOnUiThread {
                    progressBar.progress = 100
                    setStatus(
                        "Terminé : badapple.dat créé (${result.frameCount} images, " +
                            "${formatBytes(result.outputBytes)}). Copie-le dans /video sur la microSD."
                    )
                    chooseButton.isEnabled = true
                    convertButton.isEnabled = true
                }
            } catch (error: Exception) {
                runOnUiThread {
                    setStatus("Échec : ${error.message ?: "erreur de conversion inconnue"}")
                    chooseButton.isEnabled = true
                    convertButton.isEnabled = true
                }
            }
        }
    }

    private fun setStatus(message: String) { statusLabel.text = message }

    private fun formatBytes(value: Long): String = when {
        value >= 1024L * 1024L -> String.format("%.2f Mio", value / (1024.0 * 1024.0))
        value >= 1024L -> String.format("%.1f Kio", value / 1024.0)
        else -> "$value octets"
    }

    private fun card() = LinearLayout(this).apply {
        orientation = LinearLayout.VERTICAL
        setPadding(dp(16), dp(16), dp(16), dp(16))
        background = rounded(Color.rgb(20, 32, 50), dp(14))
    }

    private fun button(label: String, primary: Boolean, action: () -> Unit) =
        Button(this).apply {
            text = label
            isAllCaps = false
            textSize = 14f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(if (primary) Color.rgb(11, 18, 32) else Color.WHITE)
            background = rounded(
                if (primary) Color.rgb(142, 232, 209) else Color.rgb(31, 48, 71),
                dp(12)
            )
            setPadding(dp(12), dp(14), dp(12), dp(14))
            setOnClickListener { action() }
        }

    private fun text(value: String, size: Int, color: Int, bold: Boolean) =
        TextView(this).apply {
            text = value
            textSize = size.toFloat()
            setTextColor(color)
            if (bold) typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.START
            setLineSpacing(dp(3).toFloat(), 1f)
        }

    private fun rounded(color: Int, radius: Int) = GradientDrawable().apply {
        setColor(color)
        cornerRadius = radius.toFloat()
    }

    private fun space(height: Int) = View(this).apply {
        layoutParams = LinearLayout.LayoutParams(1, dp(height))
    }

    private fun matchWrap() = LinearLayout.LayoutParams(
        LinearLayout.LayoutParams.MATCH_PARENT,
        LinearLayout.LayoutParams.WRAP_CONTENT
    )

    private fun matchWidth() = LinearLayout.LayoutParams(
        LinearLayout.LayoutParams.MATCH_PARENT,
        LinearLayout.LayoutParams.WRAP_CONTENT
    )

    private fun dp(value: Int): Int = (value * resources.displayMetrics.density).toInt()

    override fun onDestroy() {
        executor.shutdownNow()
        super.onDestroy()
    }

    companion object {
        private const val REQUEST_VIDEO = 1101
        private const val REQUEST_OUTPUT = 1102
    }
}
