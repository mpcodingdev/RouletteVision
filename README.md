

# What is RoulleteVision?
### RouletteVision borns with the goal of using Computer Vision and AI to guess the number in which the ball will land in a roulette game, given the first movements of the ball

(this algorithm has only research purposes only and does not promote gambling)

## Resume
The project is divided in 2 main parts. The analysis alrogithm that extracts data from the video, which I'm sharing in this repo, and the Neural Network that uses the data to guess the result, which I haven't been able to make it work due to seome issues.

## Dataset

The dataset used is published on HuggingFace and is composed of 1703 pairs of videos of roulette games, the first video of the pair, which I called the input, contains the part of the roulette game where the ball is still spining around the wheel. The second video, the output, contains the last seconds of the game, where the ball stops spining around and falls into the inner part of the wheel, making some rebounds and finally falling in a number.
The code is already adapted so that accesses the videos from the dataset automatically, without having to download the videos locally

## Analysis algorithms

The code starts with 2 algorithms that first separate the raw input video into all the roulette games, and the code that separates the video into input and output; but this is a work that I already did and published the dataset with the separated videos.

So, I will focus just on the 2 main files: AN1_vid_1 and AN2_vid_2. The codes that analyze the input and output videos. 

### AN1_vid_1
Appart from tracking a number from the wheel to register the movement of it second by second; it registers the areas that the ball crosses using some points and algorithms that try to be efficient and precise.

### AN2_vid_2
It also registers the movement of the wheel and gets the position of the ball. The position is transformed into a value between 0 and 1000, this value is the position of the 0 number with respect to the right side of the roulette, being 0 when it is at 0 grades and 500 when it is at 180 grades (in the left part).
