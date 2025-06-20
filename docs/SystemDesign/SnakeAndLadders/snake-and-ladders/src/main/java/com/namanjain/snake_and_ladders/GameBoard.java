package com.namanjain.snake_and_ladders;

import lombok.AllArgsConstructor;

import java.util.List;
import java.util.Map;
import java.util.Queue;

@AllArgsConstructor
public class GameBoard {

    private Dice dice;

    private Queue<Player> nextTurn;

    private List<Jumper> snakes;

    private List<Jumper> ladders;

    private Map<String, Integer> playersCurrentPositon;

    int boardSize;

    void startGame() {
        while (nextTurn.size() > 1) {
            Player player = nextTurn.poll();

            int currentPosition = playersCurrentPositon.get(player.getPlayerName());
            int diceValue = dice.rollDice();
            int proposedPosition = currentPosition + diceValue;

            if (proposedPosition > boardSize) {
                nextTurn.offer(player);
                continue;
            }

            int finalPosition = getFinalPosition(proposedPosition, player);

            if (finalPosition == boardSize) {
                System.out.println(player.getPlayerName() + " has won the game.");
            } else {
                playersCurrentPositon.put(player.getPlayerName(), finalPosition);
                System.out.println(player.getPlayerName() + " is at position " + finalPosition);
                nextTurn.offer(player);
            }
        }
    }

    private int getFinalPosition(int position, Player player) {
        for (Jumper snake : snakes) {
            if (snake.startPoint == position) {
                System.out.println(player.getPlayerName() + " got bitten by a snake at " + position);
                return snake.endPoint;
            }
        }

        for (Jumper ladder : ladders) {
            if (ladder.startPoint == position) {
                System.out.println(player.getPlayerName() + " climbed a ladder at " + position);
                return ladder.endPoint;
            }
        }

        return position;
    }


}
