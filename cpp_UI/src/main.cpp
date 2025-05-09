/**
 * 版本：0.1
 * 作者：初阳LOCW
 * 描述：UI 主类
 */

#include <iostream>
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_ttf.h>
#undef main

#include <DFH/View.hpp>
#include <DFH/Button.hpp>
#include <DFH/TextLine.hpp>

#define FPS 60

bool isRunning = true;

SDL_Window* window;
SDL_Renderer* renderer;
SDL_Event event;

SDL_Texture* logo;
SDL_Rect l_rect;

TTF_Font* font = NULL;
SDL_Texture *inputPath, *outputPath, *authorLogo;
SDL_Rect i_rect, o_rect, a_rect;

DFH::Button* inputButton;
DFH::TextLine* inputText;
DFH::TextLine* outputText;

void CompileText(){
	TTF_Init();
	font = TTF_OpenFont("SIMHEI.TTF",48);
	if (!font) {
		std::cout << "无法打开字体，可以尝试在bin目录下运行，或者检查是否有SIMHEI.TTF文件在bin下" << std::endl;
		exit(1);
	}
	SDL_Surface* surface;
	SDL_Color color = SDL_Color{0,0,0,255};
	surface = TTF_RenderUTF8_Solid(font,"文件路径", color);
	inputPath = SDL_CreateTextureFromSurface(renderer,surface);
	SDL_FreeSurface(surface);
	surface = TTF_RenderUTF8_Solid(font,"输出路径", color);
	outputPath = SDL_CreateTextureFromSurface(renderer,surface);
	SDL_FreeSurface(surface);
	surface = TTF_RenderUTF8_Solid(font,"作者:初阳LOCW", color);
	authorLogo = SDL_CreateTextureFromSurface(renderer,surface);
	SDL_FreeSurface(surface);
	surface = TTF_RenderUTF8_Solid(font,"DFH", color);
	logo = SDL_CreateTextureFromSurface(renderer,surface);
	SDL_FreeSurface(surface);

	if (!inputPath || !outputPath || !authorLogo || !logo){
		std::cout << "无法创建文本" << std::endl;
		exit(1);
	}else{
		std::cout << "文本创建成功" << std::endl;
	}
}

void InitWindow(){
	window = SDL_CreateWindow("DFH-UI",SDL_WINDOWPOS_CENTERED,SDL_WINDOWPOS_CENTERED,800,600,SDL_WINDOW_SHOWN);
	renderer = SDL_CreateRenderer(window,-1,0);
	SDL_BlendMode mode = SDL_BlendMode::SDL_BLENDMODE_BLEND;
	SDL_GetRenderDrawBlendMode(renderer,&mode);

	CompileText();
	i_rect = SDL_Rect{50,50,60,15};
	o_rect = SDL_Rect{50,150,60,15};
	a_rect = SDL_Rect{50,550,135,15};
	l_rect = SDL_Rect{310,80,480,160};

	inputButton = new DFH::Button(SDL_Rect{620,475,60,60},SDL_Color{0,255,0,255},10,">",font,SDL_Color{0,0,0,255});

	inputText = new DFH::TextLine(SDL_Rect{20,80,240,30},SDL_Color{145, 153, 157,255},10,"",font,SDL_Color{0,0,0,255});
	outputText = new DFH::TextLine(SDL_Rect{20,170,240,30},SDL_Color{145, 153, 157,255},10,"",font,SDL_Color{0,0,0,255});

	inputButton->setListener([](){
		std::string input_path = inputText->getText();
		std::string output_path = outputText->getText();
		if (input_path.length() > 0 && output_path.length() > 0){
			input_path = "..\\..\\" + input_path;
			output_path = "..\\..\\output\\" + output_path + ".txt";
			system(("python ..\\..\\py_program\\data_formula_handler.py " + input_path + " " + output_path).c_str());
		}
	});

	std::cout << "初始化完成" << std::endl;
}

void Render(){
	SDL_SetRenderDrawColor(renderer,255,255,255,255);
	SDL_RenderClear(renderer);

	SDL_RenderCopy(renderer,inputPath,NULL,&i_rect);
	SDL_RenderCopy(renderer,outputPath,NULL,&o_rect);
	SDL_RenderCopy(renderer,authorLogo,NULL,&a_rect);
	SDL_RenderCopy(renderer,logo,NULL,&l_rect);

	inputButton->draw(renderer);
	inputText->draw(renderer);
	outputText->draw(renderer);

	SDL_RenderPresent(renderer);
}

void HandleEvent(Uint64 delta){
	if (event.type == SDL_QUIT){
		isRunning = false;
	}
	inputButton->update(event,delta);
	inputText->update(event,delta);
	outputText->update(event,delta);
}

void Loop(){
	Uint64 start, end, delta = 0;
	while (isRunning){
		start = SDL_GetTicks64();
		while (SDL_PollEvent(&event)){
			HandleEvent(delta);
		}
		Render();
		end = SDL_GetTicks64();
		delta = end - start;
		if (delta < FPS){
			SDL_Delay(FPS - delta);
		}
	}
}

void ReleaseWindowResource(){

	SDL_DestroyTexture(inputPath);
	SDL_DestroyTexture(outputPath);
	SDL_DestroyTexture(authorLogo);
	SDL_DestroyTexture(logo);
	TTF_CloseFont(font);
	TTF_Quit();

	delete inputButton;
	delete inputText;
	delete outputText;


	SDL_DestroyRenderer(renderer);
	SDL_DestroyWindow(window);

	std::cout << "释放资源完成" << std::endl;
}

int main(){
	system("chcp 65001");
	SDL_Init(SDL_INIT_EVERYTHING);
	InitWindow();
	Loop();
	ReleaseWindowResource();
	SDL_Quit();
	return 0;
}