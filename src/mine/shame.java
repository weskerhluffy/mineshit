
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;

public class MinesweeperMaster {
	public char[][] getBoard(int R, int C, int M) throws Exception{
		char[][] board = new char[R][C];

		int left = C*R - M;
		if(left == 1){
			fillBoardWithChar(board, C, R, '*');
			board[0][0] = 'c';
			return board;
		}

		if(C == 1 || R == 1)
		{
			fillBoardWithChar(board, C, R, '.');
			fillBoardForOneRow(C, R, M, board);
			return board;
		}
		if( C == 2 || R == 2){
			fillBoardWithChar(board, C, R, '.');
			fillBoardForTwoRow(C, R, M, board);
			return board;
		}
		fillBoardWithChar(board, C, R, '*');
		fillBoard(C, R, M, board);
		return board;
	}

	private void fillBoard(int C, int R, int M, char[][] board) throws Exception{
		int left = C*R - M;
		if(left < 4 || left == 5 || left == 7){ 			throw new Exception("Impossible"); 		} 		//first fill the 4 dots in this shape 		// c . 		// . . 		board[0][0] = board[0][1] = board[1][0] = board[1][1] = '.'; 		left -= 4; 		 		if(left > 1)
		{
			//then fill 2 more dots in x direction
			board[0][2] = board[1][2] = '.';
			left -= 2;
		}

		//now fill in y direction in pair of 2
		for(int iy = 2; iy < R && left > 1; iy++){
			board[iy][0] = board[iy][1] = '.';
			left -=2;
		}

		//Now fill in x direction in pair of 2, second line we had already filled
		for(int ix = 3; ix < C && left > 1; ix++){
			board[0][ix] = board[1][ix] = '.';
			left -=2;
		}

		//Now we keep on filling dots along y direction one by one
		for(int ix = 2; ix < C && left > 0; ix ++){
			for(int iy =2; iy < R && left > 0; iy++){
				board[iy][ix] = '.';
				left--;
			}
		}
		board[0][0] = 'c';
	}

	private void fillBoardForTwoRow(int C, int R, int M, char[][] board) throws Exception{
		int left = C*R - M;
		board[0][0] = 'c';
		//left =1 case handled befofe calling this function
		//if left  is from 2 to 3 its not possible
		//or if left is not a pair of 2 its not possible
		if(left < 4 || left%2 == 1){ 			throw new Exception("Impossible\n"); 		} 		if(C == 2){ 			for(int i = R-1; i >=0 & M > 0; i--){
				board[i][0] = '*';
				board[i][1] = '*';
				M -= 2;
			}
		}

		if(R == 2){
			for(int i = C-1; i >=0 & M > 0; i--){
				board[0][i] = '*';
				board[1][i] = '*';
				M -=2;
			}
		}
	}

	private void fillBoardForOneRow(int C, int R, int M, char[][] board){
		board[0][0] = 'c';
		if(C == 1){
			for(int i = R-1; i >=0 & M > 0; i--){
				board[i][0] = '*';
				M--;
			}
		}

		if(R == 1){
			for(int i = C-1; i >=0 & M > 0; i--){
				board[0][i] = '*';
				M--;
			}
		}
	}

	private void fillBoardWithChar(char[][] board, int C, int R, char c){
		for(int i=0; i < R; i++){
			for(int j=0; j < C; j++){
				board[i][j] = c;
			}
		}
	}

	private static void printBoard(char[][] board){
		for(int i =0; i < board.length; i++){
			for(int j=0; j < board[i].length; j++){
				System.out.print(board[i][j]);
			}
			System.out.println();
		}
	}

	private static void printBoardInFile(char[][] board, FileWriter writer) throws IOException{
		for(int i =0; i < board.length; i++){
			for(int j=0; j < board[i].length; j++){
				writer.write(board[i][j]);
			}
			writer.write("\n");
		}
	}
	public static void main(String[] argv) {
		try {
			long startTime = System.currentTimeMillis();
			Reader reader = new FileReader("small.in");
			BufferedReader bufReader = new BufferedReader(reader);
			String x = bufReader.readLine();
			int numOfTestCases = Integer.parseInt(x);
			int count = 0;

			File file = new File("small.out");
			FileWriter writer = new FileWriter(file);
			for(count =1; count<= numOfTestCases; count++) {
				ArrayList secondLine = getIntegerList(bufReader.readLine());
				writer.write("Case #" + count + ":\n");
				System.out.println("Case #" + count + ":");
				try{
					char[][] board = new MinesweeperMaster().getBoard((Integer)secondLine.get(0), (Integer)secondLine.get(1), (Integer)secondLine.get(2));
					printBoard(board);
					printBoardInFile(board, writer);
				}catch (Exception e) {
					// TODO: handle exception
					writer.write("Impossible\n");
					System.out.println("Impossible");
				}
			}
			writer.close();
			System.out.println("Total time = " + (System.currentTimeMillis() - startTime));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private static ArrayList getIntegerList(String s) {
		ArrayList intList = new ArrayList();
		String[] strArr = s.split(" ");
		for (String str : strArr) {
			intList.add(Integer.parseInt(str.trim()));
		}
		return intList;
	}
}
