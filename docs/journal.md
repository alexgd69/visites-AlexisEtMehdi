# Journal - TP02

## Secret historique
- Commit fautif : 36c7b0dddcee27261b564c8297b40ee8e1d1531f
- Auteur / date / fichier : Alex / 2026-10-13T10:09:42Z / app/old_settings.py
- Règle déclenchée : generic-api-key
- Remarque : le dépôt ayant été recréé, le commit du formateur n'y était pas ; le scénario a été reproduit (commit de app/old_settings.py avec un faux jeton).
- Décision : fichier supprimé par PR. Un vrai jeton aurait été révoqué côté fournisseur, car poussé sur une forge il est considéré compromis. Historique non réécrit (jeton factice ; git filter-repo changerait les SHA et obligerait à recloner). Faux positif référencé dans .gitleaksignore.

## Questions d'observation
- Dismiss stale approvals : évite qu'on fasse approuver un petit changement puis qu'on pousse du code non relu qui garde l'approbation.
- CODEOWNERS (propriétaire absent) : la PR est bloquée. Prévoir au moins 2 propriétaires par zone (ou une équipe) et un admin de secours tracé.
- Dependabot : la PR du robot doit être approuvée par un propriétaire humain, donc aucune dépendance n'entre sans revue ni tests.
- Pre-commit, nom ou valeur : gitleaks s appuie sur le nom de la variable : une fois renommée en FOO, la même valeur est acceptée et le commit passe
- Q1 : revue obligatoire (humaine, faillible), gitleaks en pre-commit (automatique mais contournable), contrôle requis gitleaks en CI (automatique, côté serveur, le plus fiable).
- Q2 : non, le pre-commit est local (hook non installé ou --no-verify). Il faut ajouter gitleaks à la CI comme contrôle requis dans le ruleset, avec Secret Scanning et Push protection.
- Q3 : quasi aucun délai, des robots scrutent les dépôts publics en continu. GitHub Secret Scanning révoque automatiquement les jetons de ses partenaires (AWS, Azure, Google, GitHub, Stripe, Slack...).
