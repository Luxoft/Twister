import javax.swing.JPanel;
import javax.swing.JTextArea;
import java.awt.Font;
import java.awt.Color;
import java.awt.BorderLayout;
import java.awt.Dimension;
import javax.swing.JLabel;
import javax.swing.BorderFactory;

public class TCDetails extends JPanel {

	JTextArea text = new JTextArea(
			"This is a sample text for helping on screen allignament");
	JLabel title = new JLabel("This is the title");

	public TCDetails() {
		setBorder(BorderFactory.createEmptyBorder(15, 10, 5, 10));
		setPreferredSize(new Dimension(450, 100));
		setMinimumSize(new Dimension(0, 0));
		setMaximumSize(new Dimension(1000, 1000));
		setLayout(new BorderLayout());
		text.setWrapStyleWord(true);
		text.setLineWrap(true);
		text.setEditable(false);
		text.setCursor(null);
		text.setOpaque(false);
		text.setFocusable(false);
		text.setFont(new Font("Arial", Font.PLAIN, 12));
		setBackground(Color.WHITE);
		text.setBackground(Color.WHITE);
		JPanel p1 = new JPanel();
		p1.setBackground(Color.WHITE);
		p1.setLayout(new BorderLayout());
		p1.add(new JLabel("Title:  "), BorderLayout.WEST);
		title.setFont(new Font("Arial", Font.PLAIN, 12));
		p1.add(title, BorderLayout.CENTER);
		JPanel p2 = new JPanel();
		p2.setBackground(Color.WHITE);
		p2.setLayout(new BorderLayout());
		p2.add(new JLabel("Description:  "), BorderLayout.NORTH);
		p2.add(text, BorderLayout.CENTER);
		add(p1, BorderLayout.NORTH);
		add(p2, BorderLayout.CENTER);
	}
}
