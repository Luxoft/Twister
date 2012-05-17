/*
   File: Browser.java ; This file is part of Twister.

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

import javax.swing.JPanel;
import javax.swing.JEditorPane;
import javax.swing.event.HyperlinkListener;
import java.net.URL;
import javax.swing.event.HyperlinkEvent;
import javax.swing.text.html.HTMLFrameHyperlinkEvent;

public class Browser {
	public JEditorPane displayEditorPane;

	public Browser() {
		displayEditorPane = new JEditorPane();
		displayEditorPane.setContentType("text/html");
		displayEditorPane.setEditable(false);
		try {
			displayEditorPane.setPage(new URL("http://" + Repository.host + ":"
					+ Repository.getHTTPServerPort()));
		} catch (Exception e) {
			System.out.println("could not get " + Repository.host + ":"
					+ Repository.getHTTPServerPort());
		}
		displayEditorPane.addHyperlinkListener(new HyperlinkListener() {
			public void hyperlinkUpdate(HyperlinkEvent e) {
				HyperlinkEvent.EventType eventType = e.getEventType();
				if (eventType == HyperlinkEvent.EventType.ACTIVATED) {
					if (!(e instanceof HTMLFrameHyperlinkEvent)) {
						try {
							displayEditorPane.setPage(e.getURL());
						} catch (Exception ex) {
							System.out.println("Could not get to:" + e.getURL());
						}
					}
				}
			}
		});
	}
}
