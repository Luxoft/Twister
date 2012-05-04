import javax.swing.JPanel;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import java.awt.Color;
import java.awt.BorderLayout;
import javax.swing.border.TitledBorder;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import java.awt.Dimension;
import javax.swing.GroupLayout;
import java.util.ArrayList;
import java.awt.FontMetrics;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Color;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.Component;
import java.util.ArrayList;

public class SuitaDetails extends JPanel {

	private JPanel defsContainer;
	private JScrollPane scroll;
	private ArrayList<DefPanel> definitions = new ArrayList<DefPanel>();
	private TitledBorder border;

	public void setEnabled(boolean enabled) {
		super.setEnabled(enabled);
		for (Component component : definitions) {
			component.setEnabled(enabled);
		}
	}

	public SuitaDetails(ArrayList<String[]> descriptions) {
		initComponents(descriptions);
	}

	public void setTitle(String title) {
		border.setTitle(title);
		repaint();
	}

	public void restart(ArrayList<String[]> descriptions) {
		removeAll();
		initComponents(descriptions);
		repaint();
	}

	private void initComponents(ArrayList<String[]> descriptions) {
		definitions.clear();
		border = BorderFactory.createTitledBorder("No suite");
		setBorder(border);
		scroll = new JScrollPane();
		defsContainer = new JPanel();
		setLayout(new BorderLayout());
		defsContainer.setBackground(new Color(255, 255, 255));
		defsContainer.setBorder(BorderFactory.createEmptyBorder(10, 0, 10, 0));
		defsContainer.setLayout(new BoxLayout(defsContainer, BoxLayout.Y_AXIS));
		scroll.setViewportView(defsContainer);
		add(scroll, java.awt.BorderLayout.CENTER);
		JLabel l = new JLabel("test");
		FontMetrics metrics = l.getFontMetrics(l.getFont());
		int width = 0;
		for (int i = 0; i < descriptions.size(); i++) {
			if (width < metrics
					.stringWidth(descriptions.get(i)[Repository.LABEL])) {
				width = metrics
						.stringWidth(descriptions.get(i)[Repository.LABEL]);
			}
		}
		for (int i = 0; i < descriptions.size(); i++) {
			boolean button = true;
			if (descriptions.get(i)[Repository.SELECTED].equals("false")) {
				button = false;
			}
			DefPanel define = new DefPanel(
					descriptions.get(i)[Repository.LABEL], button,
					descriptions.get(i)[Repository.ID], width, i, this);
			definitions.add(define);
			defsContainer.add(define);
		}
		setEnabled(false);
	}

	public int getDefsNr() {
		return definitions.size();
	}

	public ArrayList<DefPanel> getDefs() {
		return definitions;
	}

	public void clearDefs() {
		for (int i = 0; i < definitions.size(); i++) {
			definitions.get(i).setDecription("");
		}
	}

	public void setParent(Item parent) {
		for (int i = 0; i < definitions.size(); i++) {
			definitions.get(i).setParent(parent);
		}
	}

	public DefPanel getDefPanel(int i) {
		return definitions.get(i);
	}
}

class DefPanel extends JPanel {

	private JLabel description;
	private JPanel filedsGap;
	private JTextField userDefinition;
	private int index;
	private Item parent;
	private SuitaDetails container;
	private DefPanel reference;
	private String id;
	private String descriptions;

	public DefPanel(String descriptions, boolean button, String id, int width,
			final int index, SuitaDetails container) {
		this.descriptions = descriptions;
		this.id = id;
		reference = this;
		this.container = container;
		this.index = index;
		setBackground(new Color(255, 255, 255));
		setBorder(BorderFactory.createEmptyBorder(2, 20, 2, 20));
		setMaximumSize(new Dimension(32767, 30));
		setMinimumSize(new Dimension(100, 30));
		setPreferredSize(new Dimension(300, 30));
		setLayout(new BoxLayout(this, BoxLayout.LINE_AXIS));
		description = new JLabel(descriptions);
		description.setPreferredSize(new Dimension(width, 20));
		description.setMinimumSize(new Dimension(width, 20));
		description.setMaximumSize(new Dimension(width, 20));
		add(description);
		filedsGap = new JPanel();
		filedsGap.setBackground(new Color(255, 255, 255));
		filedsGap.setMaximumSize(new Dimension(20, 20));
		filedsGap.setMinimumSize(new Dimension(20, 20));
		filedsGap.setPreferredSize(new Dimension(20, 20));
		GroupLayout filedsGapLayout = new GroupLayout(filedsGap);
		filedsGap.setLayout(filedsGapLayout);
		filedsGapLayout.setHorizontalGroup(filedsGapLayout.createParallelGroup(
				GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
		filedsGapLayout.setVerticalGroup(filedsGapLayout.createParallelGroup(
				GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
		add(filedsGap);
		userDefinition = new JTextField();
		userDefinition.setText("");
		userDefinition.setMaximumSize(new Dimension(300, 100));
		userDefinition.setMinimumSize(new Dimension(50, 20));
		userDefinition.setPreferredSize(new Dimension(100, 20));
		add(userDefinition);
		userDefinition.addKeyListener(new KeyAdapter() {

			public void keyReleased(KeyEvent ev) {
				if (parent != null) {
					setParentField(userDefinition.getText(), false);
				}
			}
		});
		filedsGap = new JPanel();
		filedsGap.setBackground(new Color(255, 255, 255));
		filedsGap.setMaximumSize(new Dimension(20, 20));
		filedsGap.setMinimumSize(new Dimension(20, 20));
		filedsGap.setPreferredSize(new Dimension(20, 20));
		filedsGapLayout = new GroupLayout(filedsGap);
		filedsGap.setLayout(filedsGapLayout);
		filedsGapLayout.setHorizontalGroup(filedsGapLayout.createParallelGroup(
				GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
		filedsGapLayout.setVerticalGroup(filedsGapLayout.createParallelGroup(
				GroupLayout.Alignment.LEADING).addGap(0, 20, Short.MAX_VALUE));
		add(filedsGap);
		if (button) {
			final JButton database = new JButton("Database");
			database.setMaximumSize(new Dimension(100, 20));
			database.setMinimumSize(new Dimension(50, 20));
			database.setPreferredSize(new Dimension(80, 20));
			add(database);
			database.addActionListener(new ActionListener() {

				public void actionPerformed(ActionEvent ev) {
					DatabaseFrame frame = new DatabaseFrame(reference);
					frame.executeQuery();
					frame.setLocation((int) database.getLocationOnScreen()
							.getX() - 100, (int) database.getLocationOnScreen()
							.getY());
					frame.setVisible(true);
				}
			});
		} else {
			JPanel database = new JPanel();
			database.setBackground(Color.WHITE);
			database.setMaximumSize(new Dimension(100, 20));
			database.setMinimumSize(new Dimension(50, 20));
			database.setPreferredSize(new Dimension(80, 20));
			add(database);
		}
	}

	public void setEnabled(boolean enabled) {
		super.setEnabled(enabled);
		for (Component component : getComponents()) {
			component.setEnabled(enabled);
		}
	}

	public void setParentField(String def, boolean updateField) {
		if (updateField) {
			userDefinition.setText(def);
		}
		parent.setUserDef(index, id, def);
	}

	public String getFieldID() {
		return id;
	}

	protected void setParent(Item parent) {
		if (parent != null && parent.getType() == 2) {
			container.setTitle("Suite " + parent.getName());
			container.setEnabled(true);
		} else {
			container.setEnabled(false);
			container.setTitle("No suite");
		}
		this.parent = parent;
	}

	public String getDescription() {
		return descriptions;
	}

	public void setDecription(String desc) {
		userDefinition.setText(desc);
	}
}
