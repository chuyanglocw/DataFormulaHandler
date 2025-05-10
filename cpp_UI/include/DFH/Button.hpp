#ifndef __BUTTON_HPP__
#define __BUTTON_HPP__

#include "View.hpp"
#include <iostream>
#include<functional>
#include <SDL2/SDL_ttf.h>

namespace DFH {

	/*
	* 按钮
	*/
	class Button : public RoundView {
	public:
		SDL_Rect textRect;
		SDL_Color textColor;
		bool textChanged = false;
		std::function<void()> onClick;
		Button(SDL_Rect area, SDL_Color color, int radius, std::string textContent, TTF_Font* font, SDL_Color textColor);
		~Button();
		void draw(SDL_Renderer* renderer);
		void update(SDL_Event &event, Uint64 delta);
		void setText(std::string textContent);
		std::string getText();
		void setFont(TTF_Font* font);
		TTF_Font* getFont();
		void setListener(std::function<void()> onClick);
		void removeListener();
	private:
		std::string textContent;
		TTF_Font* font;
		SDL_Texture* text;
	};

}

#endif // __BUTTON_HPP__
