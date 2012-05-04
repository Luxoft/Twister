import javax.swing.event.MouseInputAdapter;
import javax.swing.JTabbedPane;
import java.awt.event.MouseEvent;

public class TabsReorder extends MouseInputAdapter {

	private JTabbedPane tabbed;
	private int tab;

	protected TabsReorder(JTabbedPane pane) {
		this.tabbed = pane;
		tab = -1;
	}

	public static void enableReordering(JTabbedPane pane) {
		TabsReorder instance = new TabsReorder(pane);
		pane.addMouseListener(instance);
		pane.addMouseMotionListener(instance);
	}

	public void mouseReleased(MouseEvent ev) {
		tab = -1;
	}

	public void mousePressed(MouseEvent ev) {
		tab = tabbed.getUI().tabForCoordinate(tabbed, ev.getX(), ev.getY());
	}

	public void mouseDragged(MouseEvent ev) {
		if (tab == -1) {
			return;
		}
		int targetTabIndex = tabbed.getUI().tabForCoordinate(tabbed, ev.getX(),
				ev.getY());
		if (targetTabIndex != -1 && targetTabIndex != tab) {
			boolean isForwardDrag = targetTabIndex > tab;
			tabbed.insertTab(tabbed.getTitleAt(tab), tabbed.getIconAt(tab),
					tabbed.getComponentAt(tab), tabbed.getToolTipTextAt(tab),
					isForwardDrag ? targetTabIndex + 1 : targetTabIndex);
			tab = targetTabIndex;
			tabbed.setSelectedIndex(tab);
		}
	}
}
