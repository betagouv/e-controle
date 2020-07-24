# Processus de développement et de release avec git

Nous utilisons [git-flow](https://nvie.com/posts/a-successful-git-branching-model/).

Ce modèle de développement s'appuie deux branches central qui sont *develop* et *master*.

La branche *master* reflète toujours l'état actuel en production, tandis que *develop* pointe sur les
derniers changements opérés en vue de la prochaine release.

Ces deux branches sont les principales branches du projet. Elles sont centralisées et illimitées dans le
temps.

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

On prendra l'exemple d'une feature qui fait des changements dans le user form.

On crée une branche de feature en suivant le processus suivant :
```
    $ git checkout develop
    $ git pull
    $ git checkout -b feature/update-user-form develop
```

Le développement de la feature se fait dans la nouvelle branche feature/update-user-form. On peut ajouter autant de commits que necessaire, il est encouragé de committer souvent même pour des versions intermédiaires et moches.

Une fois la feature terminée, il faut incorporer la branche dans develop:
```
    $ git checkout develop
    $ git pull develop
    $ git merge --no-ff feature/update-user-form
    $ git push origin develop
```

Note : Le flag --no-ff (no fast-forward) crée un commit de merge dans la branche develop. Si on ne le met pas, il y a des cas (le cas fast-forward) où tous les commits de la branche feature vont être ajoutés dans develop. Ce n'est pas souhaitable, car la branche feature est une branche de travail, qui peut avoir bcp de commits brouillons et pas interessants à garder. Donc on utilise toujours --no-ff.

Optionnel : supprimer la branche locale. On ne supprime pas la branche remote sur github, pour garder l'historique. (On pourra décider plus tard qu'il y a trop de branches et les supprimer, si c'est nécessaire.)
```
    $ git branch -d feature/update-user-form
```

# Réaliser une release

Pour créer une branche de release (par exemple pour la version 1.20), on suivra le processus suivant :
```
    $ git checkout develop
    $ git pull develop
    $ git checkout -b release/1.20 develop
```

Il y a 2 taches à faire dans cette nouvelle branche (on peut regarder [ce commit](https://github.com/betagouv/e-controle/commit/85a165b8) pour avoir un exemple) :
 - Ajouter des release notes dans le dossier docs/releases. On peut imiter le format des releases precedentes. On peut décider d'un nom pour la release dans ce fichier.
 - Mettre à jour la version affichée sur le site : dans templates/footer.html.

On met ces deux tâches dans un commit dans la branche release/1.20 :
```
    $ git commit -m "Updated version number"
```

Ensuite on teste la release.

On réalise les tests de recette sur au moins 2 navigateurs (3 c'est encore mieux!), dont Intenet Explorer (parce qu'il pose toujours plus de problèmes). Un test de recette doit idéalement cliquer une fois sur chaque bouton de l'interface pour vérifier qu'il marche. On peut suivre la [liste des fonctionnalités à tester](https://docs.google.com/spreadsheets/d/1YAj0BITC4nq3_IDijhncNniTphC55zr3uBrLyzeFE1A/edit#gid=638845062), qui n'est pas exhaustive. On peut aussi tester de façon plus détaillée les parties de l'interface qui ont été modifiées dans la release.

On réalise les tests de recette sur la machine de DEV. Si ils passent (on ne trouve pas de bugs), on déploie en PPROD et on refait les tests de recette en PPROD. Si ils passent, on déploie en PROD.

Dans le cas où les tests de recette trouvent des bugs, il faut les fixer dans la branche release/1.20 puis recommencer le processus de tests.

Pour ajouter le fix dans release/1.20, on peut committer directement dans release/1.20. (Si c'est un gros fix, on peut brancher depuis release/1.20 pour que ca soit plus propre, et ne laisser que le commit de merge dans release/1.20)
```
    $ git commit -m "Fixed bug with the stuff and the things"
```

Une fois que tous les tests sont passés et que la release est déployée en prod, on merge la branche release dans la branche master. La branche master ne contient que des commits qui correspondent à un release.
```
    $ git checkout master
    $ git pull
    $ git merge --no-ff release/1.20
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
```

# Réaliser un hotfix

Dans le cas où on trouve un bug en prod, après le déploiement, si on décide qu'il est important, on le fixe tout de suite. On fait un hotfix. : c'est une procédure plus rapide que de faire une release complète. Le hotfix se fait directement sur master, sans passer par develop. C'est le seul cas où le code ne commence pas par develop.

Par exemple, on se rend compte que les dates sont affichées en anglais, et on décide que c'est très grave. Pour créer une branche de hotfix, on suivra le processus suivant :
```
    $ git checkout master
    $ git pull
    $ git checkout -b hotfix/fix-dates-in-french
```

On commit le fix dans la branche (ou ou plusieurs commits) :
```
    $ git commit -m "Display the dates in french"
```

Le fix doit aussi changer le numéro de version et faire des release notes pour cette nouvelle version. Si on était précédemment à la version 1.20, alors on fait une version 1.20.1. S'inspirer de [ce commit](https://github.com/betagouv/e-controle/commit/85a165b8) (les release notes sont faciles : il n'y a que le fix qui a changé!)

On déploie cette branche sur heroku ou sur DEV et on teste que le bug est parti. On fait aussi la code review (c'est pas le moment de bacler, ca va aller directement en prod!)

Quand on est satisfait du fix, on merge la branche dans master :
```
    $ git checkout master
    $ git pull
    $ git merge --no-ff hotfix/fix-dates-in-french
```

On déploie master sur la machine de DEV, et on teste que le bug est parti. On n'est pas obligé de refaire tous les tests de recette. Ensuite on déploie sur pprod et on reteste. S'il y a encore des problèmes on les fixe.

Ensuite on fait un déploiement en prod.

On tagge master pour garder un historique des releases :
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
```

