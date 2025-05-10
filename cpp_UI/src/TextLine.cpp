#include <DFH/TextLine.hpp>

namespace DFH{
	TextLine::TextLine(SDL_Rect area, SDL_Color color, int radius, std::string text, TTF_Font* font, SDL_Color textColor) : RoundView(area, color, radius) {
		this->font = font;
		this->textColor = textColor;
		this->textContent = text;
		this->textRect = area;
		textChanged = true;
	}
	TextLine::~TextLine() {
		if (text) SDL_DestroyTexture(text);
	}
	void TextLine::draw(SDL_Renderer* renderer) {
		RoundView::draw(renderer);
		if (textChanged) {
			int tempWidth = textContent.length() * textWidth;
			textRect.w = tempWidth < area.w ? tempWidth : area.w;
			SDL_Surface* surface = TTF_RenderUTF8_Solid(font, textContent.c_str(), textColor);
			text = SDL_CreateTextureFromSurface(renderer, surface);
			SDL_FreeSurface(surface);
		}
		if (text) SDL_RenderCopy(renderer, text, NULL, &textRect);
	}
	void TextLine::update(SDL_Event &event, Uint64 delta) {
		RoundView::update(event, delta);
		if (isFocus){
			if (event.type == SDL_KEYDOWN){
				if (event.key.keysym.sym == SDLK_BACKSPACE && textContent.length() > 0) {
					textContent.erase(textContent.length() - 1);
					textChanged = true;
				}else if (event.key.keysym.sym == SDLK_RETURN) {
					SDL_StopTextInput();
					disFocus();
				}
			} else {
				SDL_StartTextInput();
				if (event.type == SDL_TEXTINPUT) {
					textContent += event.text.text;
					textChanged = true;
				}
			}
		}
	}
	void TextLine::setText(std::string text) {
		this->textContent = text;
		textChanged = true;
	}
	std::string TextLine::getText() {
		return textContent;
	}
	void TextLine::setFont(TTF_Font* font) {
		this->font = font;
		textChanged = true;
	}
	TTF_Font* TextLine::getFont() {
		return font;
	}
}