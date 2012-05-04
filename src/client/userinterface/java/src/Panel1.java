import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.event.MenuListener;
import java.io.File;
import javax.swing.JPanel;
import javax.swing.JMenuBar;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import java.awt.dnd.DropTargetListener;
import java.awt.dnd.DropTargetDragEvent;
import java.awt.dnd.DropTargetEvent;
import java.awt.dnd.DropTargetDropEvent;
import javax.swing.JSplitPane;
import java.awt.Dimension;
import javax.swing.JScrollPane;
import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeEvent;
import javax.swing.JButton;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Toolkit;
import javax.swing.JDesktopPane;
import javax.swing.JInternalFrame;
import java.awt.Container;
import java.awt.DefaultKeyboardFocusManager;
import javax.swing.JLabel;
import javax.swing.JFileChooser;
import javax.swing.event.MenuEvent;
import javax.swing.MenuSelectionManager;
import java.util.ArrayList;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.awt.FontMetrics;
import java.awt.Font;
import javax.swing.JTextField;
import javax.swing.ImageIcon;
import javax.swing.ToolTipManager;

public class Panel1 extends JPanel {
	private static final long serialVersionUID = 1L;
	public ScrollGrafic sc;
	public ExplorerPanel ep;
	private TreeDropTargetListener tdtl;
	private boolean applet;
	public JSplitPane splitPane;
	public SuitaDetails suitaDetails;
	private JLabel openedfile;
	public JButton remove;

	public Panel1(String user, final boolean applet, int width) {

		Repository.intro.text = "Started Suites interface initialization";
		Repository.intro.percent += 0.035;
		Repository.intro.repaint();
		openedfile = new JLabel();
		openedfile.setBounds(210, 23, 250, 20);
		add(openedfile);
		JButton addsuite = new JButton(new ImageIcon(Repository.addsuitaicon));
		addsuite.setToolTipText("Add Suite");
		ToolTipManager.sharedInstance().setInitialDelay(400);
		addsuite.setBounds(10, 20, 40, 25);
		add(addsuite);
		addsuite.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				sc.g.addSuiteFromButton();
			}
		});
		remove = new JButton(new ImageIcon(Repository.removeicon));
		remove.setToolTipText("Remove");
		remove.setBounds(52, 20, 40, 25);
		remove.setEnabled(false);
		add(remove);
		remove.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				sc.g.removeSelected();
			}
		});
		JButton generate = new JButton("Generate");
		generate.setBounds(94, 20, 90, 25);
		add(generate);
		suitaDetails = new SuitaDetails(Repository.getDatabaseUserFields());
		generate.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				String result = "";
				try {
					result = (String) Repository.frame.mainpanel.p2.client
							.execute("getExecStatusAll", new Object[] {});
				} catch (Exception e) {
					System.out.println("Could not connect to server");
				}
				int defsNr = suitaDetails.getDefsNr();
				boolean execute = true;
				for (int i = 0; i < Repository.getSuiteNr(); i++) {
					if (Repository.getSuita(i).getUserDefNr() < defsNr) {
						JOptionPane.showMessageDialog(Repository.frame,
								"Please set user defined fields for: "
										+ Repository.getSuita(i).getName());
						execute = false;
						break;
					}
					for (int j = 0; j < defsNr; j++) {
						if (Repository.getSuita(i).getUserDef(j)[1].length() == 0
								&& Repository.getDatabaseUserFields().get(j)[Repository.MANDATORY]
										.equals("true")) {
							JOptionPane.showMessageDialog(Repository.frame,
									"Please set user defined field at "
											+ Repository
													.getDatabaseUserFields()
													.get(j)[Repository.LABEL]
											+ " for: "
											+ Repository.getSuita(i).getName());
							execute = false;
							break;
						}
					}
					if (!execute)
						break;
				}
				if (execute) {
					if (!result.equals("running")) {
						sc.g.printXML(Repository.getTestXMLDirectory(), true,
								false);
						Repository.emptyTestRepository();
						File xml = new File(Repository.getTestXMLDirectory());
						int size = Repository.logs.size();
						for (int i = 5; i < size; i++) {
							Repository.logs.remove(5);
						}
						new XMLReader(xml).parseXML(sc.g.getGraphics(), true);
						Repository.frame.mainpanel.p2.updateTabs();
						JOptionPane.showMessageDialog(Repository.frame,
								"File successfully generated ");
					} else {
						JOptionPane
								.showMessageDialog(Repository.frame,
										"Please close Central Engine before generating");
					}
				}
			}
		});
		this.applet = applet;
		JMenuBar menu = new JMenuBar();
		menu.setLayout(null);
		menu.setBounds(0, 0, width, 20);
		final JMenu suitemenu = new JMenu("Suite");
		suitemenu.setBounds(50, 0, 50, 20);
		menu.add(suitemenu);
		JMenuItem item;
		item = new JMenuItem("Add Suite");
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				System.out.println("adding suite");
				sc.g.addSuiteFromButton();
				for (int j = 0; j < suitemenu.getMenuComponentCount(); j++) {
					suitemenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		suitemenu.add(item);
		item = new JMenuItem("Set Ep");
		suitemenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				try {
					ArrayList<Integer> temp = new ArrayList<Integer>();
					int indexsize = sc.g.getSelectedCollection().get(0).length;
					for (int j = 0; j < indexsize; j++) {
						temp.add(new Integer(sc.g.getSelectedCollection()
								.get(0)[j]));
					}
					final Item theone = sc.g.getItem(temp, false);
					File f = new File(Repository.temp
							+ System.getProperty("file.separator") + "Twister"
							+ System.getProperty("file.separator") + "EpID.txt");
					String line = null;
					InputStream in = Repository.c.get(Repository.REMOTEEPIDDIR);
					InputStreamReader inputStreamReader = new InputStreamReader(
							in);
					BufferedReader bufferedReader = new BufferedReader(
							inputStreamReader);
					StringBuffer b = new StringBuffer("");
					while ((line = bufferedReader.readLine()) != null) {
						b.append(line + ";");
					}
					bufferedReader.close();
					inputStreamReader.close();
					in.close();
					String result = b.toString();
					String[] vecresult = result.split(";");
					try {
						String ID = (String) JOptionPane.showInputDialog(sc.g,
								"Please select an EpID", "EpID's",
								JOptionPane.INFORMATION_MESSAGE, null,
								vecresult, "EpID's");
						theone.setEpId(ID);
						for (int i = 0; i < theone.getSubItemsNr(); i++) {
							sc.g.assignEpID(theone.getSubItem(i), ID);
						}
						repaint();
					} catch (Exception e) {
						e.printStackTrace();
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
				for (int j = 0; j < suitemenu.getMenuComponentCount(); j++) {
					suitemenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		item = new JMenuItem("Rename");
		suitemenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				ArrayList<Integer> temp = new ArrayList<Integer>();
				int indexsize = sc.g.getSelectedCollection().get(0).length;
				for (int j = 0; j < indexsize; j++) {
					temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));
				}
				final Item theone = sc.g.getItem(temp, false);
				String name = JOptionPane.showInputDialog(sc.g,
						"Please enter the suite name", "Suite Name",
						JOptionPane.PLAIN_MESSAGE).toUpperCase();
				FontMetrics metrics = sc.g.getGraphics().getFontMetrics(
						new Font("TimesRoman", Font.BOLD, 14));
				int width = metrics.stringWidth(name) + 140;
				theone.setName(name);
				theone.getRectangle().setSize(width,
						(int) theone.getRectangle().getHeight());
				if (theone.isVisible())
					sc.g.updateLocations(theone);
				sc.g.repaint();
				for (int j = 0; j < suitemenu.getMenuComponentCount(); j++) {
					suitemenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		item = new JMenuItem("Expand");
		suitemenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				ArrayList<Integer> temp = new ArrayList<Integer>();
				int indexsize = sc.g.getSelectedCollection().get(0).length;
				for (int j = 0; j < indexsize; j++) {
					temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));
				}
				final Item theone = sc.g.getItem(temp, false);
				theone.setVisible(true);
				sc.g.updateLocations(theone);
				sc.g.repaint();
				for (int j = 0; j < suitemenu.getMenuComponentCount(); j++) {
					suitemenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		item = new JMenuItem("Contract");
		suitemenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				ArrayList<Integer> temp = new ArrayList<Integer>();
				int indexsize = sc.g.getSelectedCollection().get(0).length;
				for (int j = 0; j < indexsize; j++) {
					temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));
				}
				final Item theone = sc.g.getItem(temp, false);
				int nr = theone.getSubItemsNr();
				for (int i = 0; i < nr; i++) {
					theone.getSubItem(i).setVisible(false);
				}
				sc.g.updateLocations(theone);
				repaint();
				for (int j = 0; j < suitemenu.getMenuComponentCount(); j++) {
					suitemenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		item = new JMenuItem("Remove");
		suitemenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				if (sc.g.getSelectedCollection().size() > 1) {
					sc.g.removeSelected();
				} else {
					ArrayList<Integer> temp = new ArrayList<Integer>();
					int indexsize = sc.g.getSelectedCollection().get(0).length;
					for (int j = 0; j < indexsize; j++) {
						temp.add(new Integer(sc.g.getSelectedCollection()
								.get(0)[j]));
					}
					final Item theone = sc.g.getItem(temp, false);
					if (theone.getPos().size() == 1) {
						int index = theone.getPos().get(0).intValue();
						Repository.getSuite().remove(theone);
						if (Repository.getSuiteNr() >= index) {
							for (int i = index; i < Repository.getSuiteNr(); i++) {
								Repository
										.getSuita(i)
										.updatePos(
												0,
												new Integer(Repository
														.getSuita(i).getPos()
														.get(0).intValue() - 1));
							}
							if (Repository.getSuiteNr() > 0) {
								Repository.getSuita(0).setLocation(
										new int[] { 5, 10 });
								sc.g.updateLocations(Repository.getSuita(0));
							}
							sc.g.repaint();
							sc.g.getSelectedCollection().clear();
						}
					} else {
						int index = theone.getPos()
								.get(theone.getPos().size() - 1).intValue();
						int position = theone.getPos().size() - 1;
						temp = (ArrayList<Integer>) theone.getPos().clone();
						temp.remove(temp.size() - 1);
						Item parent = sc.g.getItem(temp, false);
						parent.getSubItems().remove(theone);
						if (parent.getSubItemsNr() >= index) {
							for (int i = index; i < parent.getSubItemsNr(); i++) {
								parent.getSubItem(i).updatePos(
										position,
										new Integer(parent.getSubItem(i)
												.getPos().get(position)
												.intValue() - 1));
							}
						}
						sc.g.updateLocations(parent);
						sc.g.repaint();
						sc.g.getSelectedCollection().clear();
					}
					for (int j = 0; j < suitemenu.getMenuComponentCount(); j++) {
						suitemenu.getMenuComponent(j).setEnabled(false);
					}
				}
			}
		});
		for (int j = 0; j < suitemenu.getMenuComponentCount(); j++) {
			suitemenu.getMenuComponent(j).setEnabled(false);
		}

		suitemenu.addMenuListener(new MenuListener() {
			public void menuCanceled(MenuEvent ev) {
				for (int j = 0; j < suitemenu.getMenuComponentCount(); j++) {
					suitemenu.getMenuComponent(j).setEnabled(false);
				}
			}

			public void menuDeselected(MenuEvent ev) {
				if (suitemenu.getSelectedObjects() == null) {
					for (int j = 0; j < suitemenu.getMenuComponentCount(); j++) {
						suitemenu.getMenuComponent(j).setEnabled(false);
					}
				}
			}

			public void menuSelected(MenuEvent ev) {
				if (sc.g.getSelectedCollection().size() > 1) {
					suitemenu.getMenuComponent(5).setEnabled(true);
				} else {
					if (sc.g.getSelectedCollection().size() == 0) {
						suitemenu.getMenuComponent(0).setEnabled(true);
					}
					if (sc.g.getSelectedCollection().size() == 1) {
						ArrayList<Integer> temp = new ArrayList<Integer>();
						int indexsize = sc.g.getSelectedCollection().get(0).length;
						for (int j = 0; j < indexsize; j++) {
							temp.add(new Integer(sc.g.getSelectedCollection()
									.get(0)[j]));
						}
						final Item theone = sc.g.getItem(temp, false);
						if (theone.getType() == 2) {
							for (int j = 0; j < suitemenu
									.getMenuComponentCount(); j++) {
								suitemenu.getMenuComponent(j).setEnabled(true);
							}
							if (theone.getPos().size() > 1) {
								suitemenu.getMenuComponent(1).setEnabled(false);
							}
						}
					}
				}
			}
		});

		final JMenu tcmenu = new JMenu("TestCase");
		tcmenu.setBounds(100, 0, 65, 20);
		menu.add(tcmenu);

		item = new JMenuItem("Add Property");
		tcmenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				JTextField name = new JTextField();
				JTextField value = new JTextField();
				Object[] message = new Object[] { "Name", name, "Value", value };
				int r = JOptionPane.showConfirmDialog(sc.g, message,
						"Property: value", JOptionPane.OK_CANCEL_OPTION);
				if (r == JOptionPane.OK_OPTION
						&& (!(name.getText() + value.getText()).equals(""))) {
					ArrayList<Integer> temp = new ArrayList<Integer>();
					int indexsize = sc.g.getSelectedCollection().get(0).length;
					for (int j = 0; j < indexsize; j++) {
						temp.add(new Integer(sc.g.getSelectedCollection()
								.get(0)[j]));
					}
					final Item theone = sc.g.getItem(temp, false);
					ArrayList<Integer> indexpos3 = (ArrayList<Integer>) theone
							.getPos().clone();
					indexpos3.add(new Integer(theone.getSubItemsNr()));
					FontMetrics metrics = sc.g.getGraphics().getFontMetrics(
							new Font("TimesRoman", 0, 11));
					int width = metrics.stringWidth(name.getText() + ":  "
							+ value.getText()) + 38;
					Item property = new Item(name.getText(), 0, -1, -1, width,
							20, indexpos3);
					property.setValue(value.getText());
					if (!theone.getSubItem(0).isVisible())
						property.setSubItemVisible(false);
					theone.addSubItem(property);
					sc.g.updateLocations(theone);
					sc.g.repaint();
					for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
						tcmenu.getMenuComponent(j).setEnabled(false);
					}
				}
			}
		});
		item = new JMenuItem("Rename");
		tcmenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				ArrayList<Integer> temp = new ArrayList<Integer>();
				int indexsize = sc.g.getSelectedCollection().get(0).length;
				for (int j = 0; j < indexsize; j++) {
					temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));
				}
				final Item theone = sc.g.getItem(temp, false);
				String name = JOptionPane.showInputDialog(sc.g,
						"Please enter the TC name", "Suite Name",
						JOptionPane.PLAIN_MESSAGE);
				FontMetrics metrics = sc.g.getGraphics().getFontMetrics(
						new Font("TimesRoman", Font.BOLD, 13));
				int width = metrics.stringWidth(name);
				theone.setName(name);
				theone.getRectangle().setSize(width + 50,
						(int) theone.getRectangle().getHeight());
				sc.g.updateLocations(theone);
				sc.g.repaint();
				for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
					tcmenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		item = new JMenuItem("Expand");
		tcmenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				ArrayList<Integer> temp = new ArrayList<Integer>();
				int indexsize = sc.g.getSelectedCollection().get(0).length;
				for (int j = 0; j < indexsize; j++) {
					temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));
				}
				final Item theone = sc.g.getItem(temp, false);
				theone.setVisible(true);
				sc.g.updateLocations(theone);
				sc.g.repaint();
				for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
					tcmenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		item = new JMenuItem("Contract");
		tcmenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				ArrayList<Integer> temp = new ArrayList<Integer>();
				int indexsize = sc.g.getSelectedCollection().get(0).length;
				for (int j = 0; j < indexsize; j++) {
					temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));
				}
				final Item theone = sc.g.getItem(temp, false);
				theone.setVisible(false);
				sc.g.updateLocations(theone);
				sc.g.repaint();
				for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
					tcmenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		item = new JMenuItem("Switch Runnable");
		tcmenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				ArrayList<Integer> temp = new ArrayList<Integer>();
				int indexsize = sc.g.getSelectedCollection().get(0).length;
				for (int j = 0; j < indexsize; j++) {
					temp.add(new Integer(sc.g.getSelectedCollection().get(0)[j]));
				}
				final Item theone = sc.g.getItem(temp, false);
				theone.switchRunnable();
				sc.g.repaint();
				for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
					tcmenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		item = new JMenuItem("Remove");
		tcmenu.add(item);
		item.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				if (sc.g.getSelectedCollection().size() > 1) {
					sc.g.removeSelected();
				} else {
					ArrayList<Integer> temp = new ArrayList<Integer>();
					int indexsize = sc.g.getSelectedCollection().get(0).length;
					for (int j = 0; j < indexsize; j++) {
						temp.add(new Integer(sc.g.getSelectedCollection()
								.get(0)[j]));
					}
					final Item theone = sc.g.getItem(temp, false);
					sc.g.removeTC(theone);
					sc.g.getSelectedCollection().clear();
				}
				for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
					tcmenu.getMenuComponent(j).setEnabled(false);
				}
			}
		});
		for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
			tcmenu.getMenuComponent(j).setEnabled(false);
		}

		tcmenu.addMenuListener(new MenuListener() {
			public void menuCanceled(MenuEvent ev) {
				for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
					tcmenu.getMenuComponent(j).setEnabled(false);
				}
			}

			public void menuDeselected(MenuEvent ev) {
				if (tcmenu.getSelectedObjects() == null) {
					for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
						tcmenu.getMenuComponent(j).setEnabled(false);
					}
				}
			}

			public void menuSelected(MenuEvent ev) {
				if (sc.g.getSelectedCollection().size() > 1) {
					tcmenu.getMenuComponent(5).setEnabled(true);
				} else {
					if (sc.g.getSelectedCollection().size() == 1) {
						ArrayList<Integer> temp = new ArrayList<Integer>();
						int indexsize = sc.g.getSelectedCollection().get(0).length;
						for (int j = 0; j < indexsize; j++) {
							temp.add(new Integer(sc.g.getSelectedCollection()
									.get(0)[j]));
						}
						final Item theone = sc.g.getItem(temp, false);
						if (theone.getType() == 1) {
							for (int j = 0; j < tcmenu.getMenuComponentCount(); j++) {
								tcmenu.getMenuComponent(j).setEnabled(true);
							}
						}
					}
				}
			}
		});

		JMenu filemenu = new JMenu("File");
		filemenu.setBounds(10, 0, 40, 20);
		JMenuItem newuser = new JMenuItem("New suite file");
		newuser.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				String user = "";
				Repository.emptyRepository();
				try {
					user = JOptionPane.showInputDialog(null,
							"Please enter file name", "File Name", -1)
							.toUpperCase();
				} catch (NullPointerException e) {
				}
				(new XMLBuilder(Repository.getSuite())).writeXMLFile(
						Repository.getUsersDirectory()
								+ System.getProperty("file.separator") + user
								+ ".xml", false);
				Repository.frame.mainpanel.p1.sc.g.setUser(Repository
						.getUsersDirectory()
						+ System.getProperty("file.separator") + user + ".xml");
				sc.g.printXML(sc.g.getUser(), false, false);
				sc.g.updateScroll();
				sc.g.repaint();
			}
		});
		filemenu.add(newuser);
		JMenuItem changeuser = new JMenuItem("Open suite file");
		changeuser.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				File usersdirectory = new File(Repository.getUsersDirectory());
				String users[] = new String[usersdirectory.list().length];
				System.arraycopy(usersdirectory.list(), 0, users, 0,
						usersdirectory.list().length);
				String user = (String) JOptionPane.showInputDialog(null,
						"Select suite file", "Suite File", 1, null, users,
						"Suite File");
				if (user != null) {
					Repository.emptyRepository();
					Repository.frame.mainpanel.p1.sc.g.setUser(Repository
							.getUsersDirectory() + Repository.getBar() + user);
					Repository.frame.mainpanel.p1.sc.g.parseXML(new File(
							Repository.getUsersDirectory()
									+ System.getProperty("file.separator")
									+ user));
				}
				if (Repository.getSuiteNr() > 0) {
					Repository.frame.mainpanel.p1.sc.g
							.updateLocations(Repository.getSuita(0));
				}
				Repository.frame.mainpanel.p1.sc.g.repaint();
			}
		});
		filemenu.add(changeuser);
		JMenuItem saveuser = new JMenuItem("Save suite file");
		saveuser.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				if (!sc.g.getUser().equals("")) {
					if (sc.g.printXML(sc.g.getUser(), false, false))
						JOptionPane.showMessageDialog(Repository.frame,
								"File successfully saved ");
					else
						JOptionPane.showMessageDialog(Repository.frame,
								"Warning, file not saved.");
				}
			}
		});
		filemenu.add(saveuser);
		JMenuItem deleteuser = new JMenuItem("Delete suite file");
		deleteuser.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				int r = JOptionPane.showConfirmDialog(null, "Delete file "
						+ new File(sc.g.getUser()).getName() + " ?", "Delete",
						0);
				if (r == 0) {
					Repository.emptyRepository();
					try {
						new File(sc.g.getUser()).delete();
						try {
							Repository.c.cd(Repository
									.getRemoteUsersDirectory());
							Repository.c.rm(new File(sc.g.getUser()).getName());
						} catch (Exception e) {
							System.out.println("Could not delete "
									+ new File(sc.g.getUser()).getName()
									+ " from "
									+ Repository.getRemoteUsersDirectory());
							e.printStackTrace();
						}
					} catch (Exception e) {
						e.printStackTrace();
					}
					File usersdirectory = new File(Repository
							.getUsersDirectory());
					String users[] = new String[usersdirectory.list().length + 1];
					System.arraycopy(usersdirectory.list(), 0, users, 0,
							usersdirectory.list().length);
					users[users.length - 1] = "New File";
					String user = (String) JOptionPane.showInputDialog(null,
							"Please enter file name", "File Name", 1, null,
							users, "File Name");
					if (user != null) {
						if (user.equals("New File")) {
							Repository.emptyRepository();
							user = JOptionPane.showInputDialog(null,
									"Please enter file name", "File Name", -1)
									.toUpperCase();
							(new XMLBuilder(Repository.getSuite())).writeXMLFile(
									(new StringBuilder())
											.append(Repository
													.getUsersDirectory())
											.append(System
													.getProperty("file.separator"))
											.append(user).append(".xml")
											.toString(), false);
							Repository.frame.mainpanel.p1.sc.g.setUser((new StringBuilder())
									.append(Repository.getUsersDirectory())
									.append(System
											.getProperty("file.separator"))
									.append(user).append(".xml").toString());
						} else if (user != null) {
							Repository.frame.mainpanel.p1.sc.g.setUser((new StringBuilder())
									.append(Repository.getUsersDirectory())
									.append(System
											.getProperty("file.separator"))
									.append(user).toString());
							Repository.frame.mainpanel.p1.sc.g.parseXML(new File(
									(new StringBuilder())
											.append(Repository
													.getUsersDirectory())
											.append(System
													.getProperty("file.separator"))
											.append(user).toString()));
						}
					} else
						Repository.frame.mainpanel.p1.sc.g.setUser("");
					if (Repository.getSuiteNr() > 0)
						Repository.frame.mainpanel.p1.sc.g
								.updateLocations(Repository.getSuita(0));
					Repository.frame.mainpanel.p1.sc.g.repaint();
					Repository.frame.mainpanel.p1.sc.g.repaint();
				}
			}
		});
		filemenu.add(deleteuser);
		JMenuItem openlocalXML = new JMenuItem("Open from local");
		openlocalXML.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				JFileChooser chooser = new JFileChooser();
				chooser.setFileFilter(new XMLFilter());
				chooser.setCurrentDirectory(new java.io.File("."));
				chooser.setDialogTitle("Select XML File");
				if (chooser.showOpenDialog(Repository.frame) == JFileChooser.APPROVE_OPTION) {
					Repository.emptyRepository();
					sc.g.setUser(Repository.getUsersDirectory()
							+ Repository.getBar()
							+ chooser.getSelectedFile().getName());
					sc.g.parseXML(chooser.getSelectedFile());
					if (Repository.getSuiteNr() > 0)
						sc.g.updateLocations(Repository.getSuita(0));
					sc.g.repaint();
				}
			}
		});
		filemenu.add(openlocalXML);
		JMenuItem savelocalXML = new JMenuItem("Save to local");
		savelocalXML.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent ev) {
				if (!sc.g.getUser().equals("")) {
					try {
						JFileChooser chooser = new JFileChooser();
						chooser.setApproveButtonText("Save");
						chooser.setCurrentDirectory(new java.io.File("."));
						chooser.setDialogTitle("Choose Location");
						chooser.setAcceptAllFileFilterUsed(false);
						if (chooser.showOpenDialog(Panel1.this) == JFileChooser.APPROVE_OPTION) {
							if (sc.g.printXML(chooser.getSelectedFile()
									+ ".xml", false, true))
								JOptionPane.showMessageDialog(Repository.frame,
										"File successfully saved ");
							else
								JOptionPane.showMessageDialog(Repository.frame,
										"Warning, file not saved.");
						} else {
							System.out.println("No Selection");
						}
					} catch (Exception e) {
						JOptionPane.showMessageDialog(Repository.frame,
								"Warning, file not saved.");
						System.out
								.println("There was a problem in writing xml file, make sure file it is not in use.");
						e.printStackTrace();
					}
				}
			}
		});
		filemenu.add(savelocalXML);
		menu.add(filemenu);
		add(menu);
		tdtl = new TreeDropTargetListener(applet);
		sc = new ScrollGrafic(10, 32, tdtl, user, applet);
		ep = new ExplorerPanel(470, 32, tdtl, applet, Repository.c);
		setLayout(null);
		JSplitPane splitPane2 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
				new JScrollPane(ep.tree), new TCDetails());
		splitPane2.setDividerLocation(0.5);
		JSplitPane splitPane3 = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
				sc.pane, suitaDetails);
		splitPane3.setDividerLocation(0.5);
		splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, splitPane3,
				splitPane2);
		Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
		splitPane.setBounds(10, 45, (int) screenSize.getWidth() - 80, 600);
		splitPane.setDividerLocation(0.5);
		add(splitPane);

		Repository.intro.text = "Finished Suites interface initialization";
		Repository.intro.percent += 0.035;
		Repository.intro.repaint();
	}

	public void setOpenedfile(String filename) {
		openedfile.setText("Suite file: " + filename);
	}
}

class TreeDropTargetListener implements DropTargetListener {
	boolean applet;

	public TreeDropTargetListener(boolean applet) {
		this.applet = applet;
	}

	public void dragEnter(DropTargetDragEvent dropTargetDragEvent) {
	}

	public void dragExit(DropTargetEvent dropTargetEvent) {
	}

	public void dragOver(DropTargetDragEvent dropTargetDragEvent) {
		Repository.frame.mainpanel.p1.sc.g.handleDraggingLine(
				(int) dropTargetDragEvent.getLocation().getX(),
				(int) dropTargetDragEvent.getLocation().getY());
	}

	public void dropActionChanged(DropTargetDragEvent dropTargetDragEvent) {
	}

	public synchronized void drop(DropTargetDropEvent dropTargetDropEvent) {
		try {
			Repository.frame.mainpanel.p1.sc.g.clearDraggingLine();
			Repository.frame.mainpanel.p1.sc.g.drop((int) dropTargetDropEvent
					.getLocation().getX(), (int) dropTargetDropEvent
					.getLocation().getY());
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Could not get folder location");
		}
	}
}
