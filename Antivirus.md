# Guide de gestion des faux positifs d'antivirus pour Cahier de Textes

Certains logiciels antivirus peuvent signaler incorrectement Cahier de Textes comme une menace potentielle. Ceci est un faux positif dû à la nature de l'application et à son mode de compilation. Voici comment gérer cette situation :

## Pourquoi des faux positifs se produisent-ils ?

Les faux positifs peuvent se produire pour plusieurs raisons :
1. Méthodes de compilation : Certains outils de compilation, comme PyInstaller, peuvent générer des exécutables qui ressemblent à des logiciels malveillants pour les antivirus.
2. Comportement du programme : Les applications qui interagissent avec le système d'une manière inhabituelle peuvent être signalées par précaution.
3. Manque de reconnaissance : Les nouveaux logiciels n'ayant pas encore établi de réputation peuvent être considérés comme suspects.
4. Heuristiques agressives : Certains antivirus utilisent des règles de détection très sensibles qui peuvent causer des faux positifs.

Cahier de Textes est un logiciel légitime et sûr. Ces faux positifs sont des erreurs de détection et non une indication de danger réel.

## Vérification de l'authenticité

1. Vérifiez les hashes SHA-256 :
   - Hash SHA-256 de l'exécutable : 5077A8DBCEE323AA7E352A4ED0CF0D791B254789F50F894377F8725F779BBC2E
   - Hash SHA-256 du fichier zip : AD1E70903D0AFC755C3C1055E1555DA20C1AC9C59F94AF025677D55CBE3BA098

   Pour vérifier le hash sur votre machine :
   1. Ouvrez PowerShell
   2. Naviguez vers le dossier contenant Cahier_de_textes.exe ou Cahier_de_textes.zip
   3. Exécutez : `Get-FileHash -Path ".\Cahier_de_textes.exe" -Algorithm SHA256 | Select-Object Hash`
      (Remplacez "Cahier_de_textes.exe" par "Cahier_de_textes.zip" pour vérifier le fichier zip)
   4. Comparez le résultat avec les hashes officiels ci-dessus

2. Téléchargement officiel :
   Le lien de téléchargement officiel sera disponible sur la page des releases de ce dépôt GitHub.

## Ajouter Cahier de Textes aux exceptions de votre antivirus

### Windows Defender
1. Ouvrez les paramètres Windows Defender
2. Allez dans "Protection contre les virus et les menaces" > "Gérer les paramètres"
3. Sous "Exclusions", cliquez sur "Ajouter ou supprimer des exclusions"
4. Cliquez sur "Ajouter une exclusion" et sélectionnez "Fichier"
5. Naviguez vers l'emplacement de Cahier_de_textes.exe et sélectionnez-le

### Avast
1. Ouvrez Avast
2. Allez dans Menu > Paramètres > Exceptions
3. Cliquez sur "Ajouter une exception"
4. Naviguez vers l'emplacement de Cahier_de_textes.exe et sélectionnez-le

### AVG
1. Ouvrez AVG
2. Cliquez sur Menu > Paramètres > Exceptions
3. Cliquez sur "Ajouter une exception"
4. Parcourez et sélectionnez Cahier_de_textes.exe

### McAfee
1. Ouvrez McAfee
2. Cliquez sur "Paramètres" > "Quarantaine"
3. Trouvez Cahier_de_textes.exe dans la liste
4. Cliquez sur "Restaurer" et ajoutez-le aux exceptions

### Bitdefender
1. Ouvrez Bitdefender
2. Allez dans Protection > Antivirus
3. Cliquez sur Paramètres > Exceptions
4. Ajoutez le chemin vers Cahier_de_textes.exe

## Signaler un faux positif

Si votre antivirus continue de bloquer Cahier de Textes malgré ces étapes, vous pouvez signaler un faux positif à votre fournisseur d'antivirus. La plupart des éditeurs d'antivirus ont des formulaires en ligne pour signaler les faux positifs.

## Contact

Pour toute question ou problème, veuillez ouvrir une issue sur ce dépôt GitHub : https://github.com/Pacontre/Cahier_de_textes/issues

---

Dernière mise à jour : 02/07/2024