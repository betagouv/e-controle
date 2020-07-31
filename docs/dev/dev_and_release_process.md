# Processus de développement et de release avec git

Nous utilisons [git-flow](https://nvie.com/posts/a-successful-git-branching-model/).

Ce modèle de développement s'appuie deux branches centrales qui sont *develop* et *master*.

La branche *master* reflète toujours l'état actuel en production. Chacun de ses commits correspond à une release.
*develop* pointe sur les derniers changements opérés en vue de la prochaine release.

Ces deux branches sont les principales branches du projet. Elles sont centralisées et illimitées dans le temps.

D'autre part, le projet s'articule autour de trois autres types de branches :
 - feature/ ou /bugfix : utilisées pour l'addition d'une nouvelle feature, ou un bugfix. On peut utiliser les préfixes "feature" ou "bugfix" de façon interchangeable, au jugé. (bugfix n'est pas dans le git-flow standard, si on veut coller au standard, utiliser feature!)
 - release/ : utilisée pour mettre en prod les nouvelles modifications de dévelop.
 - hotfix/ : utilisée pour fixer un bug déjà présent en prod, avec une procédure accélérée par rapport à la procédure de release.

 Ces branches sont appelées branches de support, et elles intéragissent avec les branches principales
 de façon très codifiée. Par exemple :
 - feature/ et /bugfix doivent provenir de *develop* et être mergées dans *develop*
 - release/ doit provenir de *develop* et être mergée dans *develop* et *master*
 - hotfix/ doit provenir de *master* et être mergée dans *develop* et *master*

# Réaliser une feature

On prendra l'exemple d'une feature qui fait des changements dans le formulaire pour créer les utilisateurs.

## Ecrire la feature
On crée une branche de feature en suivant le processus suivant :
```
    $ git checkout develop
    $ git pull
    $ git checkout -b feature/update-user-form
```

Le développement de la feature se fait dans la nouvelle branche feature/update-user-form. On peut ajouter autant de commits que necessaire, il est encouragé de committer souvent même pour des versions intermédiaires et moches.

## Valider la feature
Une fois le code écrit, il faut qu'il soit reviewé, pour ca il faut ouvrir une PR dans github.

Il faut aussi qu'il soit testé par l'intrapreneur/PO (ou par un autre dev, mais en tout cas par une personne différente que celle qui a écrit le code) pour aider à dénicher les bugs. Pour ca, on peut déployer la branche sur heroku ou sur DEV.

La feature doit aussi être testée auprès des utilisateurs pour vérifier qu'elle est compréhensible et utile (si c'est un changement mineur ou un bugfix, on peut juger que ce n'est pas nécessaire).

## Merger la feature
Une fois la feature terminée, il faut incorporer la branche dans develop:
```
    $ git checkout develop
    $ git pull develop
    $ git merge --no-ff feature/update-user-form
    $ git push origin develop
```

Note : Le flag --no-ff (no fast-forward) crée un commit de merge dans la branche develop. Si on ne le met pas, il y a des cas (le cas fast-forward) où tous les commits de la branche feature vont être ajoutés dans develop. Ce n'est pas souhaitable, car la branche feature est une branche de travail, qui peut avoir bcp de commits brouillons et pas interessants à garder. Donc on utilise toujours --no-ff.

Optionnel : supprimer la branche locale. On ne supprime pas la branche remote sur github, pour garder l'historique. (On pourra décider plus tard qu'il y a trop de branches dans github et les supprimer, si c'est nécessaire.)
```
    $ git branch -d feature/update-user-form
```

# Réaliser une release

Quand il y a des nouveautés dans develop qu'on veut les mettre en production, on va faire une release. On prendra l'exemple de la version 1.20.

Quand est-ce qu'on release ? Dès qu'on veut. Dès qu'on a quelque chose de nouveau. Il n'y a pas de contrainte spécifique d'en faire un certain nombre par sprint.

## Créer la release
Pour créer une branche de release, on suivra le processus suivant :
```
    $ git checkout develop
    $ git pull develop
    $ git checkout -b release/1.20
    $ git push
```

Il y a 2 taches à faire dans cette nouvelle branche (on peut regarder [ce commit](https://github.com/betagouv/e-controle/commit/85a165b8) pour avoir un exemple) :
 - Ajouter des release notes dans le dossier docs/releases. On peut imiter le format des releases precedentes. On peut décider d'un nom pour la release dans ce fichier.
 - Mettre à jour la version affichée sur le site dans templates/footer.html.

On met ces deux tâches dans un commit dans la branche release/1.20 :
```
    $ git commit -m "Release notes and version number"
    $ git push
```

## Tester la release

On réalise les tests de recette sur 3 navigateurs (2 si on n'est pas motivé...), dont Intenet Explorer (parce qu'il pose toujours plus de problèmes).

Un test de recette doit idéalement cliquer une fois sur chaque bouton de l'interface pour vérifier qu'il marche. On peut suivre la [liste des fonctionnalités à tester](https://docs.google.com/spreadsheets/d/1YAj0BITC4nq3_IDijhncNniTphC55zr3uBrLyzeFE1A/edit#gid=638845062), qui n'est pas exhaustive. On peut aussi tester de façon plus détaillée les parties de l'interface qui ont été modifiées dans la release. On n'est pas obligé de faire des tests très compliqués et tordus, surtout si on a bien testé chaque feature individuellement au moment de son développement. (Si on trouve trop de bugs en prod, ou si les tests de recettes sont trop laborieux, on peut modifier cette procédure bien sur.)

On réalise les tests de recette sur la machine de DEV. Si ils passent (on ne trouve pas de bugs), on déploie en PPROD et on refait les tests de recette en PPROD.

Dans le cas où les tests de recette trouvent des bugs, il faut les fixer dans la branche release/1.20. On peut committer directement dans release/1.20. (Si c'est un gros fix, on peut brancher depuis release/1.20 pour que ca soit plus propre, et ne laisser que le commit de merge dans release/1.20)
```
  $ git checkout release/1.20
  $ git pull
  $ git commit -m 'Forgot to do the thing, fixed now'
  $ git push
```

Puis on recommence le processus de tests, jusqu'à ce qu'on soit content.

### Déployer en DEV, PPROD, PROD
Voir la [page sur le wiki interne](http://wiki-dea.ccomptes.fr/doku.php/dev/e-controle#jenkins).

## Déployer et nettoyer
Une fois que tous les tests sont passés en DEV et en PPROD, on déploie en PROD.

Pour garder la trace de cette release, on merge la branche release dans la branche master. La branche master ne contient que des commits qui correspondent à un release.
```
    $ git checkout master
    $ git pull
    $ git merge --no-ff release/1.20
    $ git push
```

On va aussi tagger le commit de master : ca fait apparaitre [une release dans la page de github](https://github.com/betagouv/e-controle/releases), et ca nous permet de garder des traces. On crée le tag en local, puis on le push sur github.
```
    $ git tag -a 1.20
    $ git push origin 1.20
```

Ensuite, il faut "backmerger" dans develop : comme on a ajouté des commits de bugfix dans release/1.20, il faut que ces commits soient ramenés aussi dans develop, pour qu'ils soient présents dans les versions suivantes.
```
    $ git checkout develop
    $ git pull
    $ git merge --no-ff release/1.20
    $ git push
```

# Réaliser un hotfix

Dans le cas où on trouve un bug en prod, après le déploiement, si on décide qu'il est important, on le fixe tout de suite. On fait un hotfix : c'est une procédure plus rapide que de faire une release complète.

Par exemple, on se rend compte que les dates sont affichées en anglais en prod, et on décide que c'est très grave. (On aurait pu aussi décider que ca peut attendre calmement la prochaine release...)

## Créer le hotfix
Le hotfix se fait directement sur master, sans passer par develop. C'est le seul cas où le code ne commence pas sa vie dans develop.

 Pour créer une branche de hotfix, on suivra le processus suivant :
```
    $ git checkout master
    $ git pull
    $ git checkout -b hotfix/fix-dates-in-french
```

On commit le fix dans la branche (ou ou plusieurs commits) :
```
    $ git commit -m "Display the dates in french"
    $ git push
```

Le fix doit aussi changer le numéro de version et faire des release notes pour cette nouvelle version. Si on était précédemment à la version 1.20, alors on fait une version 1.20.1 (version "patch"). S'inspirer de [ce commit](https://github.com/betagouv/e-controle/commit/85a165b8) (les release notes sont faciles : il n'y a que le fix qui a changé!)

## Tester le hotfix
On fait un processus similaire à quand on teste une feature.

On déploie la branche de hotfix sur heroku ou sur DEV et fait tester par l'intra/PO que le bug est parti. On fait aussi la code review (c'est pas le moment de bacler, ca va aller directement en prod!)

Quand on est satisfait du fix, on merge la branche dans master :
```
    $ git checkout master
    $ git pull
    $ git merge --no-ff hotfix/fix-dates-in-french
    $ git push
```

On déploie master sur la machine de DEV, et on teste que le bug est parti. On n'est pas obligé de refaire tous les tests de recette. Ensuite on déploie sur pprod et on reteste. S'il y a encore des problèmes on les fixe.

Ensuite on fait un déploiement en prod.

On tagge master pour garder un historique de cette release :
```
    $ git checkout master
    $ git pull
    $ git tag -a 1.20.1
    $ git push origin 1.20.1
```

Et on backmerge dans develop.
```
    $ git checkout develop
    $ git pull
    $ git merge --no-ff release/1.20.1
    $ git push
```

