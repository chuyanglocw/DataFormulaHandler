#ifndef __VIEW_HPP__
#define __VIEW_HPP__

#include <SDL2/SDL.h>

namespace DFH
{
	class View{
	public:
		SDL_Rect area;
		bool isVisible = true;
		bool isFocus = false;
		View(SDL_Rect area);
		~View();
		virtual void draw(SDL_Renderer* renderer);
		virtual void update(SDL_Event &event, Uint64 delta);
		void setVisible(bool isVisible);
		bool getVisible();
		void disFocus();
	};

	class ColorView : public View{
		public:
		SDL_Color color;
		ColorView(SDL_Rect area, SDL_Color color);
		~ColorView();
		void draw(SDL_Renderer* renderer);
	};

	/*
	* 绘制区域：
		- X型绘制
		--- area.x <= x <= area.x + radius
			绘制往下的直线，逐渐变宽
		--- area.x + radius <= x <= area.x + area.w - radius
			绘制矩形
		--- area.x + area.w - radius <= x <= area.x + area.w
			绘制往下的直线，逐渐变窄
	*/
	class RoundView : public View{
		public:
		SDL_Color color;
		int radius;
		RoundView(SDL_Rect area, SDL_Color color, int radius);
		~RoundView();
		void draw(SDL_Renderer* renderer);
	};
} // namespace DFH

#endif // __VIEW_HPP__