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
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
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
	XmlRpcClient client;
	JTabbedPane tabbed;
	private boolean cleared = true;
	JLabel cestatus;
	private boolean stoppushed = false;
	private boolean runned = false;

	public Panel2(final boolean applet) {

		Repository.intro.text = "Started Monitoring interface initialization";
		Repository.intro.percent += 0.035;
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
				try {
					String status = "";
					if (play.getText().equals("Run")) {
						for (int i = 0; i < Repository.getTestSuiteNr(); i++) {
							clearProp(Repository.getTestSuita(i));
						}
						Repository.frame.mainpanel.p2.sc.g.repaint();
						status = (String) client.execute("setExecStatusAll",
								new Object[] { 2 });
						client.execute("setStartedBy",
								new Object[] { Repository.getUser() });
						play.setText("Pause");
						play.setIcon(new ImageIcon(Repository.pauseicon));
					} else if (play.getText().equals("Resume")) {
						status = (String) client.execute("setExecStatusAll",
								new Object[] { 3 });
						play.setText("Pause");
						play.setIcon(new ImageIcon(Repository.playicon));
					} else if (play.getText().equals("Pause")) {
						status = (String) client.execute("setExecStatusAll",
								new Object[] { 1 });
						play.setText("Resume");
						play.setIcon(new ImageIcon(Repository.playicon));
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
		add(play);
		final JButton stop = new JButton("Stop", new ImageIcon(
				Repository.getStopIcon()));
		stop.setEnabled(false);
		stop.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent ev) {
				try {
					String status = (String) client.execute("setExecStatusAll",
							new Object[] { 0 });
					play.setText("Run");
					play.setIcon(new ImageIcon(Repository.playicon));
					stoppushed = true;
				} catch (Exception e) {
					e.printStackTrace();
				}
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
						try {
							XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
							config.setServerURL(new URL("http://"
									+ Repository.host + ":"
									+ Repository.getCentralEnginePort())); // !!!
																			// NU
																			// uita
																			// sa
																			// updatezi
																			// portul
																			// in
																			// mesajul
																			// de
																			// eroare
							client = new XmlRpcClient();
							client.setConfig(config);
							String result;
							while (Repository.run) {
								Thread.sleep(1000);
								result = client.execute("getExecStatusAll",
										new Object[] {}) + " ";
								String startedtime = "   Started : "
										+ result.split(";")[1];
								String elapsedtime = "   Elapsed time: "
										+ result.split(";")[2];
								String user = "   Started by: "
										+ result.split(";")[3];
								result = result.split(";")[0];
								if (result.equals("paused")) {
									cestatus.setText("CE status: paused"
											+ startedtime + elapsedtime + user);
									cleared = false;
									play.setText("Resume");
									play.setIcon(new ImageIcon(
											Repository.playicon));
								} else if (result.equals("stopped")) {
									cestatus.setText("CE status: stopped");
									stop.setEnabled(false);
									play.setText("Run");
									play.setIcon(new ImageIcon(
											Repository.playicon));
									if (runned) {
										System.out.println("Just Stopped");
										String[] buttons = { "Save to DB",
												"Export to excel", "Cancel" };
										int rc = JOptionPane.showOptionDialog(
												Repository.frame,
												"Generate statistics?",
												"Confirmation",
												JOptionPane.DEFAULT_OPTION,
												JOptionPane.QUESTION_MESSAGE,
												null, buttons, buttons[2]);
										if (rc != -1) {
											if (rc == 0) {
												System.out
														.println("Saving to DB");
												client.execute(
														"commitToDatabase",
														new Object[] {});
											} else if (rc == 1) {
												System.out
														.println("Exporting to excel..");
												generateExcel();
											}
										}
										if (!stoppushed) {
											System.out
													.println("Without stop button");
										}
										runned = false;
									}
									stoppushed = false;
								} else if (result.equals("running")) {
									stoppushed = false;
									runned = true;
									cestatus.setText("CE status: running"
											+ startedtime + elapsedtime + user);
									stop.setEnabled(true);
									cleared = false;
									play.setText("Pause");
									play.setIcon(new ImageIcon(
											Repository.pauseicon));
								}
								if (!play.isEnabled()) {
									play.setEnabled(true);
									stop.setEnabled(true);
								}

								Object result1 = client.execute(
										"getTestStatusAll", new Object[] {});
								if (result1 != null) {
									if (((String) result1).indexOf(",") != -1) {
										String[] result2 = ((String) result1)
												.split(",");
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
							System.out.println("Could not connect to: "
									+ Repository.host + " on port"
									+ Repository.getCentralEnginePort());
							e.printStackTrace();
							if (play.isEnabled()) {
								play.setEnabled(false);
								stop.setEnabled(false);
							}
						}
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

		Repository.intro.text = "Finished Monitoring interface initialization";
		Repository.intro.percent += 0.035;
		Repository.intro.repaint();
	}

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

	public void updateTabs() {
		tabbed.removeAll();
		logs.clear();
		SwingUtilities.invokeLater(new Runnable() {

			public void run() {
				try {
					for (int i = 0; i < Repository.logs.size(); i++) {
						if (i == 4) {
							continue;
						}
						Log log = new Log(500, 0, Repository.logs.get(i));
						logs.add(log);
						tabbed.addTab(Repository.logs.get(i), log.container);
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
		TabsReorder.enableReordering(tabbed);
	}

	public void updateStatuses(String[] statuses) {
		int index = 0;
		for (int i = 0; i < Repository.getTestSuiteNr(); i++) {
			index = manageSubchildren(Repository.getTestSuita(i), statuses,
					index);
		}
		Repository.frame.mainpanel.p2.sc.g.repaint();
	}

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
