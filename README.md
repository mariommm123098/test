# OCR Question Lookup Demo

This is a minimal Flask web application that demonstrates how to upload an image,
run OCR on it, and look up a matching question in a small sample dataset.

## Setup

Install system dependencies (Tesseract OCR):

```bash
sudo apt-get update && sudo apt-get install -y tesseract-ocr
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

```bash
python app.py
```

Navigate to `http://localhost:5000` in your browser and upload an image of a question.
The server will perform OCR and try to match the question text in `sample_dataset.json`.

This is a small proof-of-concept to illustrate how a full question search system
might be implemented.

## Sample Syllabus Subtopics

The following list contains example subtopics that could be referenced when cataloging questions. These are taken from a typical A-level mathematics syllabus.

### 1.1 Quadratics
- 1.1.1 Completing square for general quadratic (ax^2+bx+c)
- 1.1.2 Vertex form ((x+p)^2+q): 顶点与对称轴
- 1.1.3 Discriminant (Δ=b^2-4ac): 实根/双根/虚根判断
- 1.1.4 Solving quadratic equations by factorization & formula
- 1.1.5 Solving quadratic inequalities
- 1.1.6 Simultaneous linear & quadratic equations
- 1.1.7 Equations that are quadratic in a function (e.g. x^4-5x^2+4=0)

### 1.2 Functions
- 1.2.1 Definition, domain & range
- 1.2.2 One-to-one & onto mappings
- 1.2.3 Inverse functions
- 1.2.4 Composite functions
- 1.2.5 Horizontal & vertical shifts
- 1.2.6 Vertical & horizontal stretches & shrinks
- 1.2.7 Reflections in axes

### 1.3 Coordinate geometry
- 1.3.1 Straight line: two-point & point-slope forms
- 1.3.2 Slope & intercept form (y=mx+c)
- 1.3.3 General form (ax+by+c=0)
- 1.3.4 Distance between two points
- 1.3.5 Midpoint formula
- 1.3.6 Parallel & perpendicular lines
- 1.3.7 Circle centre–radius form ((x-a)^2+(y-b)^2=r^2)
- 1.3.8 Circle general form & completing square
- 1.3.9 Line–circle intersection & chord length
- 1.3.10 Tangent condition & equation of tangent

### 1.4 Circular measure
- 1.4.1 Degree–radian conversion
- 1.4.2 Radian definition & arc length (s=rθ)
- 1.4.3 Sector area (A=½r^2θ)
- 1.4.4 Circular segment area

### 1.5 Trigonometry
- 1.5.1 Graphs of (sin x, cos x, tan x)
- 1.5.2 Amplitude & period changes
- 1.5.3 Phase shifts & reflections
- 1.5.4 Exact values at 30°, 45°, 60°
- 1.5.5 Basic identities (sin^2x + cos^2x = 1, etc.)
- 1.5.6 Inverse-trig principal values
- 1.5.7 Solving simple trig equations in a given interval

### 1.6 Series
- 1.6.1 Binomial expansion for (a+b)^n (integer n)
- 1.6.2 Arithmetic progression: nth term
- 1.6.3 Arithmetic progression: sum of first n terms
- 1.6.4 Geometric progression: nth term
- 1.6.5 Geometric progression: sum to n terms & infinite sum

### 1.7 Differentiation
- 1.7.1 Power rule & constant multiple rule
- 1.7.2 Exponential & logarithmic derivatives
- 1.7.3 Product rule & quotient rule
- 1.7.4 Chain rule (composite functions)
- 1.7.5 Tangent & normal slopes
- 1.7.6 Stationary points & nature of extrema
- 1.7.7 Rates of change applications

### 1.8 Integration
- 1.8.1 Reverse power rule ∫ x^n dx
- 1.8.2 Definite & indefinite integrals
- 1.8.3 Constant of integration
- 1.8.4 Area under a curve by ∫_a^b f(x)dx
- 1.8.5 Volume of revolution (disc & shell methods)

