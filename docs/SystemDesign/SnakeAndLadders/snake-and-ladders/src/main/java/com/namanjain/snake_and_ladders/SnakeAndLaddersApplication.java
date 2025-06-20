package com.namanjain.snake_and_ladders;


import java.util.*;

public class SnakeAndLaddersApplication {

    public static void main(String[] args) {

        Dice dice = new Dice(1);

        Player p1 = new Player(1, "Modi");

        Player p2 = new Player(1, "Rahul");

        Queue<Player> players = new LinkedList<>();
        players.offer(p1);
        players.offer(p2);

        Jumper snake1 = new Jumper(10, 2);
        Jumper snake2 = new Jumper(99, 12);

        List<Jumper> snakes = List.of(
                snake1, snake2
        );

        Jumper ladder1 = new Jumper(5, 25);
        Jumper ladder2 = new Jumper(5, 25);

        List<Jumper> ladders = List.of(
                ladder1, ladder2
        );

        Map<String, Integer> playersCurrentPosition = new HashMap<>();
        playersCurrentPosition.put(p1.getPlayerName(), 0);
        playersCurrentPosition.put(p2.getPlayerName(), 0);

        GameBoard gameBoard = new GameBoard(
                dice, players, snakes, ladders, playersCurrentPosition, 100
        );

        gameBoard.startGame();

    }

}
