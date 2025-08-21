def maximalRectangle(matrix):
    if not matrix:
        return 0
    
    def largestRectangleArea(heights):
        stack = []
        max_area = 0
        heights.append(0)

        for i, h in enumerate(heights):
            while stack and h < heights[stack[-1]]:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] -1
                max_area = max(max_area,height*width)
            stack.append(i)

        heights.pop()
        return max_area
    
    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols
    max_area = 0
    
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == "1":
                heights[j] += 1
            else:
                heights[j] = 0
        max_area = max(max_area, largestRectangleArea(heights))

    return max_area

if __name__ == "__main__":
    print("Enter number of rows:")
    rows = int(input())
    print("Enter number of columns:")
    cols = int(input())

    print("Enter the matrix row by row (only 0 and 1, separated by space):")
    matrix = []
    for _ in range(rows):
        row = input().split()
        matrix.append(row)

    print("\nInput Matrix:")
    for r in matrix:
        print(r)

    result = maximalRectangle(matrix)
    print("\nLargest rectangle area containing only 1's:", result)