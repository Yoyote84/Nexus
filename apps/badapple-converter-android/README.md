# Nexus — BadApple Converter (Android)

Application Android native qui transforme une vidéo locale en fichier `badapple.dat` pour un lecteur RLE monochrome Cardputer ADV.

## Fonctions

- Sélection d'une vidéo depuis le sélecteur de fichiers Android.
- Décodage local avec les codecs vidéo disponibles sur Android.
- Mise à l'échelle en 240 × 135 pixels.
- Conversion monochrome avec seuil noir/blanc réglable.
- Échantillonnage à 8 images/s.
- Compression RLE et export sous le nom `badapple.dat`.
- Aucun compte, aucune API, aucun réseau et aucune permission générale de stockage.

Le fichier est créé à l'emplacement choisi dans Android. Pour le lecteur de référence, place-le sur la microSD sous `/video/badapple.dat`.

## Format binaire

Le conteneur suit le format vidéo RLE documenté dans [TurboHsu/badapple_cardputer_adv](https://github.com/TurboHsu/badapple_cardputer_adv) :

1. `uint32 little-endian` : nombre d'images.
2. Une entrée `uint32 little-endian` par image : offset relatif au début de la zone des données.
3. Les images compressées, chacune terminée par `0x80`.

Codage d'une image :

- `0x01..0x7F` : répétition de N octets `0x00`.
- `0x81..0xFF` : répétition de N octets `0xFF`.
- `0x00 <octet>` : un octet littéral.
- `0x80` : fin de l'image.

Les pixels sont packés de gauche à droite, bit de poids fort en premier. Noir = 0, blanc = 1.

## Limite de compatibilité

Le format est aligné sur le lecteur RLE du projet de référence. Le dépôt Nexus ne contient pas encore le code d'un lecteur BadApple ni de spécification propre à un autre firmware. Le nom `badapple.dat` seul ne garantit donc pas qu'un autre lecteur accepte ces octets : son décodeur doit être comparé avant de déclarer la compatibilité totale.

Le convertisseur conserve 8 images/s, cadence utilisée par le lecteur de référence.

## Construction

Avec JDK 17, Gradle 8.9 et Android SDK 35 :

```bash
gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug
```

APK généré : `app/build/outputs/apk/debug/app-debug.apk`.

Le workflow GitHub Actions de Nexus lance les tests et publie l'APK comme artefact à chaque modification de cette application.

## Utilisation

1. Ouvre BadApple Converter sur Android.
2. Appuie sur **Choisir une vidéo**.
3. Ajuste le seuil noir/blanc si nécessaire.
4. Appuie sur **Créer badapple.dat** et choisis la destination.
5. Copie le fichier dans le dossier `video` de la microSD : `/video/badapple.dat`.

Les vidéos longues créent davantage d'images et peuvent demander plusieurs minutes. La conversion est locale. L'application limite une conversion à 200 000 images et aux offsets 32 bits.
