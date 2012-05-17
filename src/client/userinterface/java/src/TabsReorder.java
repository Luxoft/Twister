/*
   File: TabsReorder.java ; This file is part of Twister.

   Copyright © 2012 , Luxoft

   Authors: Andrei Costachi <acostachi@luxoft.com>
                
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

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
