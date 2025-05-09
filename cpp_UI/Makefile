CXX = g++

src = $(wildcard src/*.cpp)
obj = $(patsubst src/%.cpp,obj/%.o,$(src))

exe = bin/DFH-UI

I-flag = -I./include
L-dir = -L./lib
libs = -lSDL2 -lSDL2_ttf -lSDL2_image
l-links = $(libs) $(L-dir)

obj/%.o : src/%.cpp
	$(CXX) $(I-flag) -c $< -o $@

$(exe): $(obj)
	$(CXX) $^ -o $@ $(I-flag) $(l-links) -mwindows

build: $(exe)

run: $(exe)
	./$(exe)