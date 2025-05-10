#include <DFH/Button.hpp>
namespace DFH
{
	Button::Button(SDL_Rect area, SDL_Color color, int radius, std::string text, TTF_Font* font, SDL_Color textColor) : RoundView(area, color, radius) {
		this->font = font;
		this->textColor = textColor;
		this->textContent = text;
		this->textRect = area;
		textChanged = true;
	}

	Button::~Button() {
		if (text) SDL_DestroyTexture(text);
	}

	void Button::draw(SDL_Renderer* renderer) {
		RoundView::draw(renderer);
		if (textChanged) {
			SDL_Surface* surface = TTF_RenderUTF8_Solid(font, textContent.c_str(), textColor);
			text = SDL_CreateTextureFromSurface(renderer, surface);
			SDL_FreeSurface(surface);
		}
		if (text) SDL_RenderCopy(renderer, text, NULL, &textRect);
	}

	void Button::update(SDL_Event &event, Uint64 delta) {
		RoundView::update(event, delta);
		if (isFocus){
			onClick();
			disFocus();
		}
	}

	void Button::setText(std::string text) {
		this->textContent = text;
		textChanged = true;
	}

	void Button::setFont(TTF_Font* font) {
		this->font = font;
		textChanged = true;
	}

	std::string Button::getText() {
		return textContent;
	}

	TTF_Font* Button::getFont() {
		return font;
	}

	void Button::setListener(std::function<void()> onClick) {
		this->onClick = onClick;
	}

	void Button::removeListener() {
		this->onClick = nullptr;
	}
}