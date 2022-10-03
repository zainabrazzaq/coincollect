# Ayesha Atif; vnd7zj
# Zainab Razzaq; nmd7ct

# GAME DESCRIPTION & FEATURES
# This game involves a player named Oswald whose goal is to earn 10 coins within 30 seconds. 
# His health is at 100% at the beginning of the game. Coins and spike balls will be
# dropping from the sky, and Oswald’s goal is to collect only the coins by
# touching the bottom of the coin. He moves left and right in order to collect
# coins and dodge spike balls. If he comes in contact with any part of a spike ball,
# he will lose 25% of his health (one heart). If he’s hit by a spike ball four times,
# his health will decline to zero (zero hearts) and the game will end.
# He will also lose the game if he is unable to collect the 10 coins within
# the 30-second time period. If he earns 10 coins within 30 seconds &
# maintains a health score of 25%, Oswald wins the game.

# Required Features
# User Input:
    # arrow keys -- movement keys for Oswald
# Window Size:
    # 800 width, 600 height
# Game Over:
    # if oswald's health drops to 0 (no hearts) or he doesn't have 10 coins
    # when the timer ends, the game ends; show game over screen
# Graphics:
    # coins, spikeballs, and hearts will appear as images

# Optional Features
# Enemies:
    # spike balls hinder Oswald from accomplishing the goal
    # if Oswald comes in contact with a spike ball, his health will decline
# Timer:
    # initial time starts at 30 seconds
    # isn't affected by anything - constantly goes down until it reach 0 seconds
# Health Bar:
    # Oswald's health starts at 100% (4 hearts)
    # goes down by 25% each time Oswald is hit by a spike ball (loses 1 heart)
# Collectibles
    # coins can be picked up by Oswald through contact
    # counter will increase by one for each coin he picks up
    # the coins will vanish after Oswald comes into contact with them

import pygame
import gamebox
import random
camera = gamebox.Camera(800,600)
screen_height = 600
screen_width = 800

# create character (oswald)
oswald = gamebox.from_image(400, 550, "character.png")
oswald.scale_by(1.4)

# collectables (coins)
coins = [
    gamebox.from_image(100, 100, "coin.png"),
    gamebox.from_image(400, 200, "coin.png"),
    gamebox.from_image(600, 300, "coin.png"),
    gamebox.from_image(250, 350, "coin.png")
]

# enemy (spike balls)
spiky = [
    gamebox.from_image(300, 100, "spiky.png"),
    gamebox.from_image(500, 240, "spiky.png"),
    gamebox.from_image(680, 200, "spiky.png"),
    gamebox.from_image(250, 150, "spiky.png"),
    gamebox.from_image(350, 320, "spiky.png"),
    gamebox.from_image(170, 70, "spiky.png")
]

# stats
score = 0
lives = 4
timer = 30

# game over
over_text = gamebox.from_text(400, 300, "YOU LOSE! GAME OVER", 50, "black")
over_box = gamebox.from_color(400, 300, "white", 500, 100)

# win game
win_text = gamebox.from_text(400, 300, "YOU WIN!", 50, "black")
win_box = gamebox.from_color(400, 300, "white", 250, 100)

def move_character(keys):
    """
    makes the character move left and right
    :param keys: keys pressed
    :return:
    """
    camera.clear('light blue')

    move_left = True
    move_right = True

    # checks whether character is touching edges
    if oswald.x >= 765:
        move_right = False
    elif oswald.x <= 35:
        move_left = False

    # check which keys are being pressed
    if pygame.K_LEFT in keys and move_left:
        oswald.x -= 8
    if pygame.K_RIGHT in keys and move_right:
        oswald.x += 8

def draw_stats():
    """
    draws the score, hearts (health bar), and timer
    :return:
    """
    score_text = gamebox.from_text(75, 25, "score: " + str(score), 36, 'red')
    camera.draw(score_text)

    for i in range(lives):
        heart = gamebox.from_image(775, 25, 'heart.png')
        heart.x -= 60 * i
        camera.draw(heart)

    global timer
    timer -= 1 / 25
    camera.draw(gamebox.from_text(700, 550, "TIMER: " + str(int(timer)), 50, "black"))

def handle_coins():
    """
    makes the coin disappear & the score increase when the
    bottom of the coin touches oswald
    :return:
    """
    global score
    for coin in coins:
        if coin.bottom_touches(oswald):
            score += 1
            coins.remove(coin)

            rand_c = random.randint(50, int(.9 * screen_width))
            if rand_c not in coins:
                coins.append(gamebox.from_image(rand_c, 0, "coin.png"))

    camera.draw(coin)

def handle_spiky():
    """
    makes the spike ball disappear & decreases the # of
    lives left when oswald touches any part of the spike ball
    :return:
    """
    global lives, heart
    for spikes in spiky:
        if spikes.touches(oswald):
            lives -= 1
            spiky.remove(spikes)

            rand_s = random.randint(50, int(.9 * screen_width))
            if rand_s not in spiky:
                spiky.append(gamebox.from_image(rand_s, 0, "spiky.png"))

    camera.draw(spikes)

def game_over(text, box):
    """
    checks if the game is over & draws things based on that
    :param text: 'You Lose! Game Over'
    :param box:
    :return: you lose, game over page
    """
    if lives == 0 or timer <= 0 and score < 10:
       camera.draw(box)
       camera.draw(text)
       camera.display()
       return True
    return False

def winning(text, box):
    """
    checks if the user won & draws things based on that
    :param text: 'You Win!'
    :param box:
    :return: you win page
    """
    if score >= 10 and lives >= 1 and timer <= 0:
        camera.draw(box)
        camera.draw(text)
        camera.display()
        return True
    return False


def tick(keys):
    """
    runs the animation
    :param keys: keys pressed
    :return:
    """
    camera.clear('light blue')

    if game_over(over_text, over_box):
        return
    if winning(win_text, win_box):
        return

    move_character(keys)
    draw_stats()
    handle_coins()
    handle_spiky()

    for coin in coins:
        camera.draw(coin)

        # control speed of coins
        coin.yspeed = 0
        coin.yspeed += 7
        coin.y += coin.yspeed

        # repeat
        if coin.y > 610:
            coin.y = -5

    for spikes in spiky:
        camera.draw(spikes)

        # control speed of spike balls
        spikes.yspeed = 0
        spikes.yspeed += 6
        spikes.y += spikes.yspeed

        # repeat
        if spikes.y > 610:
            spikes.y = -5

    camera.draw(oswald)
    camera.display()

gamebox.timer_loop(30,tick)

# CITATIONS (links for graphics)
# https://i.pinimg.com/originals/61/48/82/614882c242f67f87c30537dc44ce83bb.png
# https://is5-ssl.mzstatic.com/image/thumb/Purple1/v4/f8/3b/fa/f83bfa53-119e-010a-a7e3-7549ef614cb5/source/512x512bb.jpg
# https://w7.pngwing.com/pngs/935/758/png-transparent-minecraft-video-game-health-game-result.png
# https://www.pinpng.com/pngs/m/320-3207611_gold-coins-cartoon-coin-transparent-background-hd-png.png