import javax.swing.JPanel;
import java.awt.GradientPaint;
import java.awt.Color;
import java.awt.Dimension;
import java.util.Random;
import javax.swing.JScrollPane;
import javax.swing.JScrollBar;
import java.awt.event.MouseEvent;
import java.awt.Graphics2D;
import java.awt.geom.RectangularShape;
import java.awt.Font;
import javax.swing.JTabbedPane;
import javax.swing.event.ChangeListener;
import javax.swing.event.ChangeEvent;
import javax.swing.JScrollPane;
import java.awt.Toolkit;

public class Panel3 extends JPanel {

	private static final long serialVersionUID = 1L;
	public JTabbedPane pane;
	public JScrollPane panel, panel4, panel2, panel5;
	public Browser browser;

	public Panel3() {

		Repository.intro.text = "Started Details interface initialization";
		Repository.intro.percent += 0.035;
		Repository.intro.repaint();
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		setLayout(null);
		pane = new JTabbedPane();
		pane.setBounds(5, 5, (int) screenSize.getWidth() - 65, 630);
		browser = new Browser();
		panel5 = new JScrollPane(browser.displayEditorPane);
		pane.add("Browser", panel5);
		add(pane);

		Repository.intro.text = "Finished Details interface initialization";
		Repository.intro.percent += 0.035;
		Repository.intro.repaint();
	}
}
