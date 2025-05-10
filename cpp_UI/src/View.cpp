#include <DFH/View.hpp>
#include <math.h>
namespace DFH
{
    View::View(SDL_Rect area) {
		this->area = area;
	}
    View::~View() {}
    void View::draw(SDL_Renderer *renderer) {}
    void View::update(SDL_Event &event, Uint64 delta) {
		if (event.type == SDL_MOUSEBUTTONDOWN) {
			if (event.button.button == SDL_BUTTON_LEFT) {
				SDL_Point point = {event.button.x, event.button.y};
				if (SDL_PointInRect(&point, &area)) {
					isFocus = true;
				}else {
					isFocus = false;
				}
			}
		}
	}
	void View::setVisible(bool visible) {
		isVisible = visible;
	}
	bool View::getVisible() {
		return isVisible;
	}
	void View::disFocus() {
		isFocus = false;
	}

	ColorView::ColorView(SDL_Rect area, SDL_Color color) : View(area) {
		this->color = color;
	}
	ColorView::~ColorView() {}
	void ColorView::draw(SDL_Renderer *renderer) {
		if (!isVisible) {
			return;
		}
		SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
		SDL_RenderFillRect(renderer, &area);
	}

	RoundView::RoundView(SDL_Rect area, SDL_Color color, int radius = 3) : View(area) {
		this->color = color;
		this->radius = radius;
	}
	RoundView::~RoundView() {}
	void RoundView::draw(SDL_Renderer *renderer) {
		if (!isVisible) {
			return;
		}
		SDL_SetRenderDrawColor(renderer, color.r, color.g, color.b, color.a);
		for (int x = area.x; x <= area.x + radius; x++) {
			int dx = x - area.x;
			int dy = sqrt(radius * radius - (radius-dx) * (radius-dx));
			SDL_RenderDrawLine(renderer,x,area.y + radius - dy, x, area.y + area.h + dy - radius -1);
			SDL_RenderDrawLine(renderer,area.x+area.w-dx,area.y + radius - dy,area.x+area.w-dx, area.y + area.h + dy - radius -1);
		}
		SDL_Rect area = {this->area.x + radius, this->area.y, this->area.w - 2 * radius, this->area.h};
		SDL_RenderFillRect(renderer, &area);
	}
} // namespace DFH
