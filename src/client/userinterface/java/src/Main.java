import javax.swing.UIManager;
import javax.swing.UIManager.LookAndFeelInfo;
import javax.swing.SwingUtilities;

public class Main {

	public static void main(String args[]) {
		Repository.initialize(false, "tsc-server", null);
	}
}
