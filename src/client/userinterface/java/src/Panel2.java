/*
File: Panel2.java ; This file is part of Twister.

Copyright (C) 2012 , Luxoft

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
import java.io.File;
import java.io.PrintStream;
import javax.swing.JPanel;
import javax.swing.JButton;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.IOException;
import javax.swing.ImageIcon;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.BorderFactory;
import javax.swing.JSplitPane;
import java.awt.Dimension;
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeEvent;
import java.net.URL;
import java.net.URLConnection;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import javax.swing.JTabbedPane;
import java.util.ArrayList;
import java.net.URL;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.JPopupMenu;
import javax.swing.JMenuItem;
import java.awt.Toolkit;
import java.io.FileInputStream;
import java.io.FileWriter;
import javax.swing.JFileChooser;
import javax.swing.JLabel;
import java.awt.Color;
import javax.swing.JOptionPane;
import javax.swing.JFrame;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import jxl.write.Label;
import jxl.write.WritableWorkbook;
import jxl.write.WritableSheet;
import java.io.File;
import jxl.Workbook;
import jxl.CellView;
import javax.swing.SwingUtilities;

public class Panel2 extends JPanel {

	private static final long serialVersionUID = 1L;
	ScrollGraficTest sc;
	ArrayList<Log> logs = new ArrayList<Log>();
	JSplitPane splitPane;
	JTabbedPane tabbed;
	private boolean cleared = true;
	JLabel cestatus;
	private boolean stoppushed = false;
	private boolean runned = false;
	private JButton stop;

	public Panel2(final boolean applet) {
		Repository.intro
				.setStatus("Started Monitoring interface initialization");
		Repository.intro.addPercent(0.035);
		Repository.intro.repaint();
		sc = new ScrollGraficTest(0, 0, applet);
		tabbed = new JTabbedPane();
		splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, sc.pane, tabbed);
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		splitPane.setBounds(10, 45, (int) screenSize.getWidth() - 80, 600);
		splitPane.setDividerLocation(0.5);
		setLayout(null);
		add(splitPane);
		final JButton play = new JButton("Run", new ImageIcon(
				Repository.getPlayIcon()));
		play.setEnabled(false);
		play.setBounds(10, 5, 105, 25);
		play.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent ev) {
				play(play);
			}
		});
		add(play);
		stop = new JButton("Stop", new ImageIcon(Repository.getStopIcon()));
		stop.setEnabled(false);
		stop.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent ev) {
				stop(play);
			}
		});
		stop.setBounds(121, 5, 95, 25);
		add(stop);
		cestatus = new JLabel("CE status: ");
		cestatus.setBounds(225, 12, 550, 25);
		cestatus.setForeground(new Color(100, 100, 100));
		add(cestatus);
		try {
			new Thread() {

				public void run() {
					while (Repository.run) {
						askCE(play);
					}
				}
			}.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
		new Thread() {

			public void run() {
				while (sc.g.getGraphics() == null) {
					try {
						Thread.sleep(50);
					} catch (Exception e) {
						System.out
								.println("Thread interrupted at getting Graphics");
					}
				}
				File xml = new File(Repository.getTestXMLDirectory());
				if (xml.length() > 0) {
					new XMLReader(xml).parseXML(sc.g.getGraphics(), true);
				} else {
					try {
						System.out.println(xml.getCanonicalPath()
								+ " has no content");
					} catch (Exception e) {
						e.printStackTrace();
					}
				}
				updateTabs();
			}
		}.start();
		Repository.intro
				.setStatus("Finished Monitoring interface initialization");
		Repository.intro.addPercent(0.035);
		Repository.intro.repaint();
	}

	/*
	 * get status from ce and adjust accordingly
	 */
	public void askCE(JButton play) {
		try {
			String result;
			while (Repository.run) {
				Thread.sleep(1000);
				result = Repository.getRPCClient().execute("getExecStatusAll",
						new Object[] {})
						+ " ";
				String startedtime = "   Started : " + result.split(";")[1];
				String elapsedtime = "   Elapsed time: " + result.split(";")[2];
				String user = "   Started by: " + result.split(";")[3];
				result = result.split(";")[0];
				if (result.equals("paused")) {
					Repository.window.mainpanel.p1.setGenerate(false);
					cestatus.setText("CE status: paused" + startedtime
							+ elapsedtime + user);
					cleared = false;
					play.setText("Resume");
					play.setIcon(new ImageIcon(Repository.playicon));
				} else if (result.equals("stopped")) {
					Repository.window.mainpanel.p1.setGenerate(true);
					cestatus.setText("CE status: stopped");
					stop.setEnabled(false);
					play.setText("Run");
					play.setIcon(new ImageIcon(Repository.playicon));
					if (runned) {
						userOptions();
					}
					stoppushed = false;
				} else if (result.equals("running")) {
					Repository.window.mainpanel.p1.setGenerate(false);
					stoppushed = false;
					runned = true;
					cestatus.setText("CE status: running" + startedtime
							+ elapsedtime + user);
					stop.setEnabled(true);
					cleared = false;
					play.setText("Pause");
					play.setIcon(new ImageIcon(Repository.pauseicon));
				}
				if (!play.isEnabled()) {
					play.setEnabled(true);
					stop.setEnabled(true);
				}
				Object result1 = Repository.getRPCClient().execute(
						"getFileStatusAll", new Object[] {});
				if (result1 != null) {
					if (((String) result1).indexOf(",") != -1) {
						String[] result2 = ((String) result1).split(",");
						updateStatuses(result2);
					} else {
						String[] result2 = { (String) result1 };
						updateStatuses(result2);
					}
				}
			}
		} catch (Exception e) {
			try {
				Thread.sleep(1000);
			} catch (Exception ex) {
				ex.printStackTrace();
			}
			System.out.println("Could not connect to: " + Repository.host
					+ " on port" + Repository.getCentralEnginePort());
			e.printStackTrace();
			if (play.isEnabled()) {
				play.setEnabled(false);
				stop.setEnabled(false);
			}
		}
	}

	/*
	 * Prompt user to save to db or localy in excel file
	 */
	public void userOptions() {
		System.out.println("Just Stopped");
		String[] buttons = { "Save to DB", "Export to excel", "Cancel" };
		String resp = CustomDialog.showButtons(Panel2.this,
				JOptionPane.QUESTION_MESSAGE, JOptionPane.DEFAULT_OPTION, null,
				buttons, "Confirmation", "Generate statistics?");
		if (!resp.equals("NULL")) {
			if (resp.equals("Save to DB")) {
				System.out.println("Saving to DB");
				try {
					Repository.getRPCClient().execute("commitToDatabase",
							new Object[] {});
				} catch (Exception e) {
					System.out
							.println("Could not comunicate with ce through RPC");
					e.printStackTrace();
				}
			} else if (resp.equals("Export to excel")) {
				System.out.println("Exporting to excel..");
				generateExcel();
			}
		}
		if (!stoppushed) {
			System.out.println("Without stop button");
		}
		runned = false;
	}

	/*
	 * stop CE from executing
	 */
	public void stop(JButton play) {
		try {
			String status = (String) Repository.getRPCClient().execute(
					"setExecStatusAll", new Object[] { 0 });
			play.setText("Run");
			play.setIcon(new ImageIcon(Repository.playicon));
			stoppushed = true;
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/*
	 * Handle play button pressed based on play previous status
	 */
	public void play(JButton play) {
		try {
			String status = "";
			if (play.getText().equals("Run")) {
				for (int i = 0; i < Repository.getTestSuiteNr(); i++) {
					clearProp(Repository.getTestSuita(i));
				}
				Repository.window.mainpanel.p2.sc.g.repaint();
				status = (String) Repository.getRPCClient().execute(
						"setExecStatusAll", new Object[] { 2 });
				Repository.getRPCClient().execute("setStartedBy",
						new Object[] { Repository.getUser() });
				play.setText("Pause");
				play.setIcon(new ImageIcon(Repository.pauseicon));
			} else if (play.getText().equals("Resume")) {
				status = (String) Repository.getRPCClient().execute(
						"setExecStatusAll", new Object[] { 3 });
				play.setText("Pause");
				play.setIcon(new ImageIcon(Repository.playicon));
			} else if (play.getText().equals("Pause")) {
				status = (String) Repository.getRPCClient().execute(
						"setExecStatusAll", new Object[] { 1 });
				play.setText("Resume");
				play.setIcon(new ImageIcon(Repository.playicon));
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/*
	 * Ask and generate excel file with the suites and their status
	 */
	public boolean generateExcel() {
		try {
			JFileChooser chooser = new JFileChooser();
			chooser.setApproveButtonText("Save");
			chooser.setCurrentDirectory(new java.io.File("."));
			chooser.setDialogTitle("Choose Location");
			chooser.setAcceptAllFileFilterUsed(false);
			if (chooser.showOpenDialog(this) == JFileChooser.APPROVE_OPTION) {
				WritableWorkbook workbook = Workbook.createWorkbook(new File(
						chooser.getSelectedFile() + ".xls"));
				WritableSheet sheet = workbook.createSheet("First Sheet", 0);
				int columns = 4 + Repository.getTestSuita(0).getUserDefNr();
				Label label;
				String titles[] = new String[columns];
				titles[0] = "Suite";
				titles[1] = "TC";
				titles[2] = "EPId";
				titles[3] = "Status";
				for (int i = 4; i < columns; i++) {
					titles[i] = Repository.getTestSuita(0).getUserDef(i - 4)[0];
				}
				for (int i = 0; i < columns; i++) {
					label = new Label(i, 0, titles[i]);
					sheet.addCell(label);
				}
				int index = 1;
				for (int i = 0; i < Repository.getTestSuiteNr(); i++) {
					Item suita = Repository.getTestSuita(i);
					index = addToExcel(sheet, suita, index, columns);
				}
				CellView view = new CellView();
				view.setAutosize(true);
				for (int i = 0; i < columns; i++) {
					sheet.setColumnView(i, view);
				}
				sheet.getSettings().setVerticalFreeze(1);
				workbook.write();
				workbook.close();
				return false;
			} else {
				System.out.println("No Selection");
				return false;
			}
		} catch (Exception e) {
			System.out
					.println("There was a problem in writing excel file, make sure file it is not in use.");
			e.printStackTrace();
			boolean continua = true;
			while (continua) {
				continua = generateExcel();
				if (!continua) {
					return continua;
				}
			}
			return false;
		}
	}

	/*
	 * method to populate excel row with suites data
	 * 
	 * sheet - excel sheet to be populated element - the Item to populate excel
	 * data with index - row numbel columns - the columns to populate
	 */
	public int addToExcel(WritableSheet sheet, Item element, int index,
			int columns) {
		if (element.getType() == 1) {
			Label label;
			try {
				label = new Label(0, index, element.getFirstSuitaParent(true)
						.getName());
				sheet.addCell(label);
				label = new Label(1, index, element.getName());
				sheet.addCell(label);
				label = new Label(2, index, element.getFirstSuitaParent(true)
						.getEpId());
				sheet.addCell(label);
				label = new Label(3, index, element.getSubItem(0).getValue());
				sheet.addCell(label);
				for (int i = 4; i < columns; i++) {
					label = new Label(i, index, element.getParent(true)
							.getUserDef(i - 4)[1]);
					sheet.addCell(label);
				}
				index++;
			} catch (Exception e) {
				System.out.println("Could not write to excel sheet");
				e.printStackTrace();
			}
			return index;
		} else if (element.getType() == 2) {
			for (int i = 0; i < element.getSubItemsNr(); i++) {
				index = addToExcel(sheet, element.getSubItem(i), index, columns);
			}
			return index;
		}
		return index;
	}

	/*
	 * Update tabs based on the logs found in repository
	 */
	public void updateTabs() {
		tabbed.removeAll();
		logs.clear();
		SwingUtilities.invokeLater(new Runnable() {

			public void run() {
				try {
					for (int i = 0; i < Repository.getLogs().size(); i++) {
						if (i == 4) {
							continue;
						}
						Log log = new Log(500, 0, Repository.getLogs().get(i));
						logs.add(log);
						tabbed.addTab(Repository.getLogs().get(i),
								log.container);
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
		TabsReorder.enableReordering(tabbed);
	}

	/*
	 * update TC satatus
	 */
	public void updateStatuses(String[] statuses) {
		int index = 0;
		for (int i = 0; i < Repository.getTestSuiteNr(); i++) {
			index = manageSubchildren(Repository.getTestSuita(i), statuses,
					index);
		}
		Repository.window.mainpanel.p2.sc.g.repaint();
	}

	/*
	 * interpret status value and asign it to item
	 */
	public int manageSubchildren(Item item, String[] statuses, int index) {
		int index2 = index;
		if (item.getType() == 1 && statuses.length > index2) {
			if (statuses[index2].equals("10")) {
				item.getSubItem(0).setValue("pending");
			} else if (statuses[index2].equals("1")) {
				item.getSubItem(0).setValue("running");
			} else if (statuses[index2].equals("2")) {
				item.getSubItem(0).setValue("pass");
			} else if (statuses[index2].equals("3")) {
				item.getSubItem(0).setValue("fail");
			} else if (statuses[index2].equals("4")) {
				item.getSubItem(0).setValue("skipped");
			} else if (statuses[index2].equals("5")) {
				item.getSubItem(0).setValue("stopped");
			} else if (statuses[index2].equals("6")) {
				item.getSubItem(0).setValue("not executed");
			} else if (statuses[index2].equals("7")
					|| statuses[index2].equals("8")) {
				item.getSubItem(0).setValue("timeout");
			} else if (statuses[index2].equals("9")) {
				item.getSubItem(0).setValue("waiting");
			}
			index2++;
			return index2;
		} else if (item.getType() == 2) {
			for (int i = 0; i < item.getSubItemsNr(); i++) {
				index2 = manageSubchildren(item.getSubItem(i), statuses, index2);
			}
			return index2;
		}
		return index2;
	}

	/*
	 * return status of stop button
	 */
	public boolean getStopStatus() {
		return stop.isEnabled();
	}

	/*
	 * assign value Pending to item
	 */
	public void clearProp(Item item) {
		if (item.getType() == 1) {
			item.getSubItem(0).setValue("Pending");
		} else if (item.getType() == 2) {
			for (int i = 0; i < item.getSubItemsNr(); i++) {
				clearProp(item.getSubItem(i));
			}
		}
	}
}
