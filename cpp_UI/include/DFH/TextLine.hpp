#ifndef __TEXTLINE_HPP__
#define __TEXTLINE_HPP__

#include <DFH/View.hpp>
#include <SDL2/SDL_ttf.h>
#include <iostream>

namespace DFH {

	/*
	* 文本行
	*/
	class TextLine : public RoundView {
	public:
		TTF_Font* font;
		SDL_Rect textRect;
		SDL_Color textColor;
		std::string textContent;
		SDL_Texture* text;
		bool textChanged = false;
		int textWidth = 16;
		TextLine(SDL_Rect area, SDL_Color color, int radius, std::string text, TTF_Font* font, SDL_Color textColor);
		~TextLine();
		void draw(SDL_Renderer* renderer);
		void update(SDL_Event &event, Uint64 delta);
		void setText(std::string textContent);
		std::string getText();
		void setFont(TTF_Font* font);
		TTF_Font* getFont();
	};

}

#endif // __TEXTLINE_HPP__