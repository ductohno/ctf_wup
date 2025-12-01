import heapq
import json
import requests
import re
import ast
# Define the goal state
GOAL_STATE = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

# Possible moves: (row_change, col_change)
MOVES = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

#change this
next_puzzle="/p/1960999365fe41b3be48f200213f864c"
HEADERS = {"Content-Type": "application/json"}

for i in range(300):
    url = f"http://chall.ehax.tech:8001{next_puzzle}"
    def manhattan_distance(state):
        """Calculate the Manhattan distance heuristic."""
        distance = 0
        for r in range(4):
            for c in range(4):
                if state[r][c] == 0:
                    continue
                goal_r, goal_c = divmod(state[r][c] - 1, 4)
                distance += abs(r - goal_r) + abs(c - goal_c)
        return distance

    def find_empty_tile(state):
        """Find the coordinates of the empty tile (0)."""
        for r in range(4):
            for c in range(4):
                if state[r][c] == 0:
                    return r, c

    def apply_move(state, move):
        """
        Move the empty tile if possible.

        Parameters:
            state (list): The current puzzle state.
            move (str): One of the keys in MOVES ('up', 'down', 'left', 'right').

        Returns:
            list or None: The new state after the move, or None if the move is not possible.
        """
        r, c = find_empty_tile(state)
        dr, dc = MOVES[move]
        new_r, new_c = r + dr, c + dc

        if 0 <= new_r < 4 and 0 <= new_c < 4:
            new_state = [row[:] for row in state]
            new_state[r][c], new_state[new_r][new_c] = new_state[new_r][new_c], new_state[r][c]
            return new_state
        return None

    def print_state(state):
        """Print the state in a readable format."""
        for row in state:
            print(row)
        print()  # Print an empty line for separation

    def solve_15_puzzle(initial_state):
        """Solve the 15-puzzle using the A* algorithm."""
        priority_queue = []
        heapq.heappush(priority_queue, (0, initial_state, []))
        visited = set()

        while priority_queue:
            cost, state, path = heapq.heappop(priority_queue)
            state_tuple = tuple(tuple(row) for row in state)

            if state == GOAL_STATE:
                return path  # Return the sequence of moves

            if state_tuple in visited:
                continue
            visited.add(state_tuple)

            for move in MOVES:
                new_state = apply_move(state, move)
                if new_state:
                    new_path = path + [move]  # Save the move's name
                    new_cost = len(new_path) + manhattan_distance(new_state)
                    heapq.heappush(priority_queue, (new_cost, new_state, new_path))

        return None  # No solution found

    def change_move_to_oxy(solution_moves):
        list_move = {
            'up': [-1, 0],
            'down': [1, 0],
            'left': [0, -1],
            'right': [0, 1]
        }
        for i in range(len(solution_moves)):
            solution_moves[i]=list_move[solution_moves[i]]
        return solution_moves

    # Initial state
    response_initial_state=requests.get(url)
    pattern = r"\[\[\d+(?:,\s*\d+)*\](?:,\s*\[\d+(?:,\s*\d+)*\])*\]"

    match = re.search(pattern, response_initial_state.text)
    if match:
        result = match.group()
        print("Found:", result)
        initial_state = ast.literal_eval(result)
        print(initial_state)
    else:
        exit()

    solution_moves = solve_15_puzzle(initial_state)
    if solution_moves is not None:
        print("Sequence of moves:", solution_moves)
        # Print each state as the moves are applied
        current_state = initial_state
        print("Initial state:")
        print_state(current_state)
        for i, move in enumerate(solution_moves):
            print(f"Move {i}: {move}")
            current_state = apply_move(current_state, move)
            print_state(current_state)
    else:
        print("No solution found.")
    solution_moves=change_move_to_oxy(solution_moves)
    # Send the moves to the server
    response = requests.post(url+"/check", json={"movements": solution_moves}, headers=HEADERS)
    print(response.text)
    response_parsed=json.loads(response.text)
    if (response_parsed["next_puzzle"]):
        next_puzzle=response_parsed["next_puzzle"]
        print(next_puzzle)
    else:
        print(next_puzzle)
        exit()
