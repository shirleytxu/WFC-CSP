/*
* Author: Shirley Xu 
 * Date:   June 26, 2021
 * Desc:   Allows the user to set up a sample image for Wave Function Collapse Algorithm by clicking 
 *         cells to cycle through colors-- white, black, red. If user right clicks with mouse, creates 
 *         a piece of generative art using patterns from user's sample image, favoring patterns with    
 *         more red color to create canvas that is most varied and exciting.  
 */

int upperLeftX = 100;  // Horizontal location of upper left corner of the grid
int upperLeftY = 100;  // Vertical location of upper left corner of the grid
int numCells = 8;      // The grid will have numCells Cells both across and down
int cellSize = 50;    // The pixel length of one side of a Cell

Grid grid;             // The Grid object that manages all Cells
IntList allColors;     // A list of possible colors for the Cells
int[] entropy = new int[(numCells - 1) * (numCells - 1)];

color white = color(255);      
color black = color(0);
color red = color(255, 0, 0);

/*
*  The Grid manages all of the Cells.
 */
class Grid {

  ArrayList<Cell> allCells;  // We store all Cells in this ArrayList

  Grid() {
    this.allCells = new ArrayList<Cell>();
  }

  /*
  *  Display all Cells.
   */
  void display() {
    for (Cell cell : allCells) {
      cell.display();
    }
  }

  /*
  *  Create the Cells and pack them into the ArrayList allCells.
   */
  void createCells() {
    for (int col = 0; col < numCells; col++) {
      for (int row = 0; row < numCells; row++) {
        Cell s = new Cell(row, col, 0, cellSize);
        this.allCells.add(s);
      }
    }
  }

  /*
  *  Find the clicked Cell and cycle it to the next available color.
   */
  void cycleCellColor(int mousex, int mousey) {
    for (Cell cell : allCells) {
      if (cell.isClicked(mousex, mousey)) {
        cell.cycleColor();
      }
    }
  }
}

/*
*  A Cell is a square region in the grid that can take on a color.
 */
class Cell {

  int row;           // The index (not pixel location) of the Cell's row
  int col;           // The index (not pixel location) of the Cell's column
  int colorIndex;    // The index (in allColors) of the color that the Cell currently has
  int sideLength;    // The length of a Cell's side in pixels

  Cell(int row, int col, int clr, int sl) {
    this.row = row;
    this.col = col;
    this.colorIndex = clr;
    this.sideLength = sl;
  }

  /*
  *  Display a Cell.
   */
  void display() {
    fill(color(allColors.get(this.colorIndex)));

    // Convert the row and column indices to pixel locations:
    int xloc = upperLeftX + this.row * this.sideLength;
    int yloc = upperLeftY + this.col * this.sideLength;
    rect(xloc, yloc, this.sideLength, this.sideLength);
  }

  /*
  *  Determine if a given Cell has been clicked by the user.
   *  @param mousex : The horizontal location of the mouse click.
   *  @param mousey : The vertical location of the mouse click.
   *  @return True if the click came from inside this Cell.
   */
  boolean isClicked(int mousex, int mousey) {
    int x = upperLeftX + this.row * this.sideLength;
    int y = upperLeftY + this.col * this.sideLength;
    int sideHalf = sideLength / 2;
    if (abs(mousex - (x + sideHalf)) < sideHalf && abs(mousey - (y + sideHalf)) < sideHalf) {
      return true;
    }
    return false;
  }

  /*
  *  Switch this Cell to the next color in allColors.
   */
  void cycleColor() {
    this.colorIndex = (this.colorIndex + 1) % allColors.size();
  }

  /* 
   * Changes color index of cell 
   */
  void setColor(int colorIndex) {
    this.colorIndex = colorIndex;
  }
}

/*
*  Handles mouse clicks by the user.
 *  Left mouse button: Cycle the clicked Cell to the next available color.
 *  Right mouse button: Create generative art based on patterns present on the user's sample image. 
 */
void mousePressed() {
  if (mouseButton == LEFT) {
    grid.cycleCellColor(mouseX, mouseY);
  } else {                                 // Right Click 
    int counter = 0;                       // For printing output in a square form
    for (Cell cell : grid.allCells) {
      counter++;
      if (counter % numCells == 0) println();
    }
    println();
    run();
  }
} 

boolean isPatternViable(IntList currentPattern, ArrayList<IntList> previousPatterns, int row, int col) { 
  // Returns true if current pattern is viable (overlaps with nearby cells), false if not viable 
  int lastPatternIndex = previousPatterns.size() - 1; 
  if (col == 0) {  // First column
    if (row == 0) {
     // First column, first row: all patterns valid
      return true;
    } else {
      // First column, remaining rows: must check left pattern to validate  
      if (previousPatterns.get(lastPatternIndex).get(1) == currentPattern.get(0) && previousPatterns.get(lastPatternIndex).get(3) == currentPattern.get(2)) {
        return true;
      }
      return false;
    }
  } else 
  {
    // Remaining columns
    if (row == 0) {
      // Remaining columns, first row: must check left pattern to validate
      if (previousPatterns.get(lastPatternIndex).get(1) == currentPattern.get(0) && previousPatterns.get(lastPatternIndex).get(3) == currentPattern.get(2)) {
      
        return true;
      }
      return false;
    } else {
      // Remaining columns, remaining rows: must check both left pattern and above pattern to validate
      if (previousPatterns.get(lastPatternIndex).get(1) == currentPattern.get(0) && previousPatterns.get(lastPatternIndex).get(3) == currentPattern.get(2)) {
        if (previousPatterns.get(lastPatternIndex + 1 - numCells).get(2) == currentPattern.get(0) && previousPatterns.get(lastPatternIndex + 1 - numCells).get(3) == currentPattern.get(1)) {  
          return true;
        }
      }
      return false;
    }
  }
}

ArrayList<IntList> createBiasedList(ArrayList<IntList> viablePatterns) {
  // Create list with all viable patterns, with a bias towards red colored patterns
  ArrayList<IntList> biasedList = new ArrayList<IntList>();
  for (IntList pat : viablePatterns) { 
    for (int p : pat) {
      biasedList.add(pat);  // Add all patterns that work to the list once
      if (p == 2) { // If cell is red, add pattern again to increase chances of being picked  
        biasedList.add(pat);
      }
    }
  }
  return biasedList;
}

/*
*  Top-level function for running the WFC algorithm.
 */
void run() {
  ArrayList<IntList> patterns = patternsFromSample();
  ArrayList<IntList> patternsFinal = new ArrayList<IntList>(numCells * numCells); 
  background(50);
  grid = new Grid();
  grid.createCells(); 
  
  int patternIndex = 0; 
  IntList previousPattern = patterns.get(patternIndex);    // Store previous pattern

  for (int row = 0; row < (numCells - 1); row++) {
    for (int col = 0; col < (numCells - 1); col++) {
      ArrayList<IntList> viablePatterns = new ArrayList<IntList>();

      for (IntList currentPattern : patterns) {
        // Loops through all patterns, adds all viable patterns to list 
        boolean viable = isPatternViable(currentPattern, patternsFinal, row, col);
        if (viable) {
          viablePatterns.add(currentPattern);
        }
      } 
      
      // If no patterns work, choose a random pattern 
      if (viablePatterns.size() == 0){
        int randomIndex = int(random(0, patterns.size()));
        viablePatterns.add(patterns.get(randomIndex));
      }
      
      ArrayList<IntList> biasedList = createBiasedList(viablePatterns);
      
      // Randomly choose a pattern from list of all viable patterns to use as pattern for this Cell
      int rand = int(random(0, biasedList.size()));
      IntList currentPattern = biasedList.get(rand);
      patternsFinal.add(currentPattern);
      
      // Upper left cell 
      Cell cell1 = grid.allCells.get(col * numCells + row);
      cell1.setColor(currentPattern.get(0));

      // Upper right cell
      Cell cell2 = grid.allCells.get(col * numCells + row + 1);
      cell2.setColor(currentPattern.get(1));

      // Lower left cell
      Cell cell3 = grid.allCells.get((col+1) * numCells + row);
      cell3.setColor(currentPattern.get(2));
      
      // Lower right cell
      Cell cell4 = grid.allCells.get((col+1) * numCells + row + 1);
      cell4.setColor(currentPattern.get(3));
      previousPattern = currentPattern;
    }
  }
  grid.display();
}

// preprocessing, starting at random 
/*
*  Collect all unique patterns from the user's sample.
 */
ArrayList<IntList> patternsFromSample() {
  // Let's make an IntList containing the color indices of the Cells,
  // as in: {0, 0, 0, 0, 0, 2, 1, 0, ..., 0, 0}

  IntList colors = new IntList();

  for (Cell cell : grid.allCells) {
    colors.append(cell.colorIndex);
  }

  for (int i = 0; i < (numCells - 1) * (numCells - 1); i++) {
    entropy[i] = 1;
  }

  // Then we will iterate through this IntList to create patterns of
  // length 4, as in: { [0, 0, 0, 2], [0, 0, 2, 1], ..., [2, 0, 0, 0] }

  ArrayList<IntList> patterns = new ArrayList<IntList>();

  for (int row = 0; row < (numCells - 1); row++) {
    for (int col = 0; col < (numCells - 1); col++) {

      // Find a new pattern in the user's input:
      IntList pattern = new IntList();

      pattern.append(colors.get(col + row * numCells));
      pattern.append(colors.get(col + row * numCells + 1));
      pattern.append(colors.get(col + (row + 1) * numCells));
      pattern.append(colors.get(col + (row + 1) * numCells + 1));

      // For debugging:
      for (int p : pattern) print (p);
      println(); 

      // Is the new pattern unique? If so, then add it to patterns:
      int patternIndex = findPatternIndex(patterns, pattern); 
      if (patternIndex == -1) {
        patterns.add(pattern);
      } else {
        entropy[patternIndex] += 1;
      }
    }
  }
 
  return patterns;
  // We want all rotations of these patterns
  // We only want unique patterns
}

int findPatternIndex(ArrayList<IntList> patterns, IntList pattern) {
  for (int patternIndex = 0; patternIndex < patterns.size(); patternIndex++) {
    if (isEqual(patterns.get(patternIndex), pattern)) {
      return patternIndex;
    }
  }
  return -1;
} 

boolean isEqual(IntList pattern1, IntList pattern2) {
  if (pattern1.size() != pattern2.size()) return false;
  for (int loc = 0; loc < pattern1.size(); loc++) {
    if (pattern1.get(loc) != pattern2.get(loc)) return false;
  }
  return true;
}

void setup() {
  size(600, 600);
  rectMode(CORNER);

  // Create the grid and its Cells:
  grid = new Grid();
  grid.createCells();

  // Add some colors to our allColors list:
  allColors = new IntList();
  allColors.append(white);
  allColors.append(black);
  allColors.append(red);
}

void draw() {
  background(50);
  grid.display();
}
