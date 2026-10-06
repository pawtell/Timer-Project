#include <iostream>
#include <raylib.h>
#include <deque>
#include <raymath.h>
using namespace std;

Color green = {173, 204, 96, 255};
Color darkGreen = {43, 51, 25, 255};

int cell_size = 30;     //30 * 25 = 750. our game resolution. each cell is invisible
int cell_count = 25;    //will reference to make everything in these chunk sizes. 
int offset = 75; //determines the width of he border lines. 

double last_update_time = 0; 



bool Event_Triggered(double interval){
    double currentTime = GetTime();
    cout<<currentTime<<endl;
    
    if(currentTime - last_update_time >= interval){
        last_update_time = currentTime;
        return true;
    }
    return false;
}

bool Element_in_deque(Vector2 element, deque<Vector2> deque){
    for(unsigned int i=0; i<deque.size(); i++){
        if(Vector2Equals(deque[i], element)){
            return true;
        }
    }
    return false;
}



class Snake{
public:
deque<Vector2> body = {Vector2{6,9}, Vector2{5,9}, Vector2{4,9} };
Vector2 direction = {1,0};  // a 2D position/vector. so x_direction=1, y_direction=0...
bool add_segment = false;  //if snake ate food, if not we dont add a segment. 

void Draw(){
    for(unsigned int i=0; i<body.size(); i++){
        float x = body[i].x;
        float y = body[i].y;
        Rectangle segment = Rectangle{offset+x*cell_size, offset+y*cell_size, (float)cell_size, (float)cell_size};  //construct segment of that piece of body.
        DrawRectangleRounded(segment, 0.5, 6, darkGreen);  //higher the segment, the smoother the segment. draw each segment of body after it was constructed.
    }
}
void Update(){
    body.push_front(Vector2Add(body[0], direction));  //depending on the direction, move body that x,-x,y,-1 direction. 
    if(add_segment == true){  //if snake ate food. 
        add_segment = false;  //after snake ate food. set back to false because food respawned and snake is not eating it anymore. 
    }else{
        body.pop_back();  //as snake moves and push_front is called based on direction, we have to pop the last element, or else snake will grow forever and leave a footprint on the game. 
    }

}
void Reset(){  //called in gameover function, we just reset the snake position back to its default starting position. 
    body = {Vector2{6,9}, Vector2{5,9}, Vector2{4,9}};
    direction = {1, 0};
}
};



class Food{
public:
Vector2 position;  //we still need the position.x and position.y declared for the random x,y generation to work.
Texture2D texture; 

Food(deque<Vector2> snakeBody){  //remember a constructor is called when creating a food object. 
    Image image = LoadImage("Graphics/food.png");
    texture = LoadTextureFromImage(image);
    UnloadImage(image);
    position = Generate_Random_Position(snakeBody);  //snakebody created in random position. 
}
~Food(){
    UnloadTexture(texture);
}

void Draw(){
    //drawing a darkgreen 30x30px sized square, we can use the position vector to identify the location of x,y
    //DrawRectangle(position.x*cell_size, position.y*cell_size, cell_size, cell_size, darkGreen);
    //instead if we wanna use the texture loaded from the image, we replace DrawRectangle() function with....
    DrawTexture(texture, offset+position.x * cell_size, offset+position.y*cell_size, WHITE);  //color is tint applied to image
}

Vector2 Generate_Random_Cell(){
    float x = GetRandomValue(0, cell_count-1);  //can be 0 - 25-1 IMAGINARY cells available on the map
    float y = GetRandomValue(0, cell_count-1);  //can be 0 - 25-1 IMAGINARY cells available on the map
    return Vector2{x, y};
}
Vector2 Generate_Random_Position(deque<Vector2> snakeBody){
    Vector2 position = Generate_Random_Cell();
    while(Element_in_deque(position, snakeBody)){
        position = Generate_Random_Cell();
    }
    return position;
}
};



class Game{
public:
Snake snake = Snake();
Food food = Food(snake.body);
bool running = true;
int score = 0;
Sound eatSound;
Sound wallSound;

Game(){
    InitAudioDevice();
    eatSound = LoadSound("Sounds/eat.mp3");
    wallSound = LoadSound("Sounds/wall.mp3");
}
~Game(){
    UnloadSound(eatSound);
    UnloadSound(wallSound);
    CloseAudioDevice();
}

void Draw(){
    food.Draw();
    snake.Draw();
}
void Update(){
    if(running){
        snake.Update();
        Check_collision_with_food();
        Check_collision_with_edges();   
        Check_collision_with_tail();     
    }
}
void Check_collision_with_food(){
    if(Vector2Equals(snake.body[0], food.position)){
        food.position = food.Generate_Random_Position(snake.body);
        snake.add_segment = true;  //snake ate food, set to true. global variable, when snake.update() it will run code.
        score++;
        PlaySound(eatSound);
    }
}
void Check_collision_with_edges(){
    if(snake.body[0].x == cell_count || snake.body[0].x == -1){  //head hit the right or left edge of the screen
        Game_Over();
    }
    if(snake.body[0].y == cell_count || snake.body[0].y == -1){
        Game_Over();
    }
}
void Check_collision_with_tail(){
    deque<Vector2> headlessBody = snake.body; //create a copy of the snake's body
    headlessBody.pop_front();
    if(Element_in_deque(snake.body[0], headlessBody)){
        Game_Over();
    }
}
void Game_Over(){
    snake.Reset();
    food.position = food.Generate_Random_Position(snake.body);
    running = false;
    score = 0;
    PlaySound(wallSound);
}
};



int main () {

    const int playable_screen_width = cell_size*cell_count;
    const int playable_screen_height = cell_size*cell_count;

    InitWindow(2*offset + playable_screen_width, 2*offset + playable_screen_height, "SNAKE GAME");
    SetTargetFPS(60);

    Game game = Game();

    while(WindowShouldClose() == false){
        BeginDrawing(); //important or else game will crash and wont close lol. 


        if(Event_Triggered(0.2)){
            game.Update();
        }

        if(IsKeyPressed(KEY_UP) && game.snake.direction.y != 1){  //making sure the snake is not already moving DOWN
            game.snake.direction = {0, -1};
            game.running = true;
        }
        if(IsKeyPressed(KEY_DOWN) && game.snake.direction.y != -1){  //snake only moves down if not moving up
            game.snake.direction = {0, 1};
            game.running = true;
        }
        if(IsKeyPressed(KEY_LEFT) && game.snake.direction.x != 1){  //snake move left if not moving right
            game.snake.direction = {-1, 0};
            game.running = true;
        }
        if(IsKeyPressed(KEY_RIGHT) && game.snake.direction.x != -1){  //snake move right if not moving left. 
            game.snake.direction = {1, 0};
            game.running = true;
        }


        int currenttime = GetTime();
        ClearBackground(green);  //fill screen with that color, clear previous frames too. 
        DrawRectangleLinesEx(Rectangle{(float)offset-5, (float)offset-5, (float)cell_size*cell_count+10, (float)cell_size*cell_count+10}, 5, darkGreen);
        DrawText(TextFormat("%i", game.score), offset-5, offset+cell_size*cell_count+10, 40, darkGreen);
        DrawText(TextFormat("%i", currenttime), 300, 300, 40, WHITE);
        DrawText("RetroSnake", offset-5, 10, 60, darkGreen);
        game.Draw();

        EndDrawing();
    }
    CloseWindow();

    return 0;
}