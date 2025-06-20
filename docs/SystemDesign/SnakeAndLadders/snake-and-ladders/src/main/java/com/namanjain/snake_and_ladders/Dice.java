package com.namanjain.snake_and_ladders;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.Date;
import java.util.Random;

@Getter
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class Dice {

    private int numberOfDice;

    private Random randomObj;

    Dice(int numberOfDice) {
        this.numberOfDice = numberOfDice;
        randomObj = new Random(new Date().getTime());
    }


    int rollDice() {
        return randomObj.nextInt(1, 7);
    }
}
