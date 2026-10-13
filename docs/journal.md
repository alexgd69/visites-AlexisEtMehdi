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

# Journal - TP03

## Mesures
- Durée du job avant matrice et cache : 47 s
- Première exécution avec matrice et cache (cache miss) : 46 s (py3.12) et 53 s (py3.13)
- Exécution avec cache restauré (cache hit) : 48 s (py3.12) et 45 s (py3.13)
- Checks requis dans le ruleset : "test (py3.12)" et "test (py3.13)"
- Ce qu'act ne sait pas faire : upload-artifact échoue (ACTIONS_RUNTIME_TOKEN absent, pas de service d'artefacts GitHub en local) et le cache de GitHub n'est pas fourni. Le reste (ruff, pre-commit, pytest) s'exécute comme sur GitHub.
- Remarque : le dépôt ayant été recréé, app/ et tests/ ont été reconstitués avant le TP03.

## Réponses
- Déclenchement sur la PR : GitHub exécute le workflow du commit de merge de la PR, qui contient ci.yml, même absent de main.
- Seuil de couverture : utile, mais pas 100 % (tests sans valeur, blocages pour des lignes triviales) ; environ 80 % est un compromis. Couverture mesurée : 95 %, app/main.py est le fichier le moins couvert.
- Matrice : 2 checks sur la PR, les deux sont requis dans le ruleset.
- Bypass : un admin peut fusionner sans attendre les contrôles ; droit réservé aux admins, tracé dans l'historique de la PR et l'audit log du dépôt.
- act : ne remplace pas GitHub Actions pour valider une PR (les checks requis viennent de la forge) ; indispensable pour déboguer sans pousser ou sans forge accessible.

## Questions d'observation
- Q1 : le pipeline dure de 45 à 53 s. L'installation des dépendances est petite ici, donc le cache n'apporte presque rien (écart dans le bruit) ; le temps vient surtout du démarrage de l'exécuteur, de l'environnement pre-commit (téléchargement du hook gitleaks) et des tests.
- Q2 : ce qui empêche de contourner le pipeline, c'est le ruleset (contrôles requis + PR + signature) ; sans ruleset, le pipeline n'est qu'un avis.
- Q3 : pour Gitea Actions, presque rien ne change (le dossier devient .gitea/workflows) ; pour GitLab CI, il faut réécrire tout le fichier (.gitlab-ci.yml) avec les mêmes concepts (jobs, stages, cache, artifacts, matrix via parallel:matrix).

# Journal - TP03

## Mesures
- Durée du job avant matrice et cache : 47 s
- Première exécution avec matrice et cache (cache miss) : 46 s (py3.12) et 53 s (py3.13)
- Exécution avec cache restauré (cache hit) : 48 s (py3.12) et 45 s (py3.13)
- Checks requis dans le ruleset : "test (py3.12)" et "test (py3.13)"
- Ce qu'act ne sait pas faire : upload-artifact échoue (ACTIONS_RUNTIME_TOKEN absent, pas de service d'artefacts GitHub en local) et le cache de GitHub n'est pas fourni. Le reste (ruff, pre-commit, pytest) s'exécute comme sur GitHub.
- Remarque : le dépôt ayant été recréé, app/ et tests/ ont été reconstitués avant le TP03.

## Réponses
- Déclenchement sur la PR : GitHub exécute le workflow du commit de merge de la PR, qui contient ci.yml, même absent de main.
- Seuil de couverture : utile, mais pas 100 % (tests sans valeur, blocages pour des lignes triviales) ; environ 80 % est un compromis. Couverture mesurée : 95 %, app/main.py est le fichier le moins couvert.
- Matrice : 2 checks sur la PR, les deux sont requis dans le ruleset.
- Bypass : un admin peut fusionner sans attendre les contrôles ; droit réservé aux admins, tracé dans l'historique de la PR et l'audit log du dépôt.
- act : ne remplace pas GitHub Actions pour valider une PR (les checks requis viennent de la forge) ; indispensable pour déboguer sans pousser ou sans forge accessible.

## Questions d'observation
- Q1 : le pipeline dure de 45 à 53 s. L'installation des dépendances est petite ici, donc le cache n'apporte presque rien (écart dans le bruit) ; le temps vient surtout du démarrage de l'exécuteur, de l'environnement pre-commit (téléchargement du hook gitleaks) et des tests.
- Q2 : ce qui empêche de contourner le pipeline, c'est le ruleset (contrôles requis + PR + signature) ; sans ruleset, le pipeline n'est qu'un avis.
- Q3 : pour Gitea Actions, presque rien ne change (le dossier devient .gitea/workflows) ; pour GitLab CI, il faut réécrire tout le fichier (.gitlab-ci.yml) avec les mêmes concepts (jobs, stages, cache, artifacts, matrix via parallel:matrix).
