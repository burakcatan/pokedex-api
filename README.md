# Pokedex API

This is a simple API to list and filter pokemons, their types and moves.

## List & Filter

Data has been divided into three main categories:
* Pokemons
* Types
* Moves
### List ###
To list all pokemons, types or moves:

```
$ curl http://localhost:5000/get/pokemons
$ curl http://localhost:5000/get/types
$ curl http://localhost:5000/get/moves
```
These will bring all pokemons, types or moves.

### Filter 
```
$ curl http://localhost:5000/get/pokemons?Name=Pikachu
$ curl http://localhost:5000/get/types?Name=Water
``` 
You can filter pokemons with their attributes such as Name, BaseAttack, BaseDefense, BaseStamina, Weight, Height etc.
Some attributes may have return more than one pokemon. 
```
$ curl http://localhost:5000/get/pokemons?BaseAttack=148
$ curl http://localhost:5000/get/types?effectiveAgainst=Dark
```
You can apply multiple filters.
```
$ curl http://localhost:5000/get/pokemons?BaseAttack=148&BaseStamina=130&Type=Steel
```

## Sort
There are 4 functions that help you sorting the output: `max`, `min`, `sortby` and `order`.
```
$ curl http://localhost:5000/get/moves?max=damage
$ curl http://localhost:5000/get/types?min=weakAgainst
$ curl http://localhost:5000/get/pokemons?max=Special Attack(s)
```
You can combine filters with sorting:
```
$ curl http://localhost:5000/get/pokemons?BaseAttack=148&sortby=Weight&order=desc
```

## Count
Counting pokemons, types or moves are pretty straightforward. Replacing /get/ with /count/ will return the count.
```
$ curl http://localhost:5000/count/moves
$ curl http://localhost:5000/count/pokemons?type=Electric
$ curl http://localhost:5000/count/pokemons?Weight=120
```
