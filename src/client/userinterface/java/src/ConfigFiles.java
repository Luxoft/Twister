/*
File: ConfigFiles.java ; This file is part of Twister.

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

import javax.swing.JPanel;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import net.sf.vfsjfilechooser.VFSJFileChooser;
import net.sf.vfsjfilechooser.accessories.DefaultAccessoriesPanel;
import org.apache.commons.vfs.FileObject;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.dom.DOMSource;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerConfigurationException;
import org.w3c.dom.Element;
import java.io.File;
import java.io.FileInputStream;
import javax.xml.transform.Result;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Comment;
import javax.swing.JOptionPane;
import java.util.ArrayList;
import com.jcraft.jsch.ChannelSftp.LsEntry;
import java.io.InputStream;
import java.io.FileOutputStream;
import java.io.ByteArrayOutputStream;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import java.awt.Component;
import java.awt.HeadlessException;
import javax.swing.JDialog;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.Container;
import java.awt.Color;
import javax.swing.plaf.ComponentUI;
import java.awt.GridLayout;
import javax.swing.BorderFactory;
import javax.swing.BoxLayout;
import java.awt.Font;
import javax.swing.border.TitledBorder;
import javax.swing.JTextArea;
import java.awt.Dimension;
import javax.swing.Box;
import javax.swing.BorderFactory;
import javax.swing.border.BevelBorder;
import java.awt.BorderLayout;
import javax.swing.SwingUtilities;
import net.sf.vfsjfilechooser.VFSJFileChooser.RETURN_TYPE;
import net.sf.vfsjfilechooser.utils.VFSUtils;
import javax.swing.AbstractAction;
import javax.swing.JFrame;
import javax.swing.JProgressBar;
import javax.swing.JComboBox;
import java.util.Arrays;

public class ConfigFiles extends JPanel {

	VFSJFileChooser fileChooser;
	private static JTextField ttcpath, tMasterXML, tUsers, tepid, tlog,
			trunning, tname, thardwareconfig, tdebug, tsummary, tinfo, tcli,
			tdbfile, temailfile, tceport, traPort, thttpPort;
	JPanel paths;

	public ConfigFiles(Dimension screensize) {

		paths = new JPanel();
		paths.setBackground(Color.WHITE);
		paths.setLayout(null);
		paths.setPreferredSize(new Dimension(970, 1060));
		paths.setBorder(BorderFactory.createBevelBorder(BevelBorder.LOWERED));
		setLayout(null);
		ttcpath = new JTextField();
		addPanel(
				"TestCase Source Path",
				"Master directory with the test cases that can be run by the framework",
				ttcpath, Repository.TESTSUITEPATH, 5, true, null);
		tMasterXML = new JTextField();
		addPanel(
				"Master XML TestSuite",
				"Location of the XML that is generated from the user interface to run on Central Engine",
				tMasterXML, Repository.XMLREMOTEDIR, 73, true, null);
		tUsers = new JTextField();
		addPanel("Suites Path", "Location of suites XML files", tUsers,
				Repository.REMOTEUSERSDIRECTORY, 141, true, null);
		tepid = new JTextField();
		addPanel("EP name File",
				"Location of the file that contains the Ep name list", tepid,
				Repository.REMOTEEPIDDIR, 209, true, null);
		tlog = new JTextField();
		addPanel(
				"Logs Path",
				"Location of the directory that stores the logs that will be monitored",
				tlog, Repository.LOGSPATH, 277, true, null);
		JPanel p7 = new JPanel();
		p7.setBackground(Color.WHITE);
		TitledBorder border7 = BorderFactory.createTitledBorder("Log Files");
		border7.setTitleFont(new Font("Arial", Font.PLAIN, 14));
		border7.setBorder(BorderFactory.createLineBorder(new Color(150, 150,
				150), 1));
		p7.setBorder(border7);
		p7.setLayout(new BoxLayout(p7, BoxLayout.Y_AXIS));
		p7.setBounds(80, 345, 800, 190);
		paths.add(p7);
		JTextArea log2 = new JTextArea(
				"All the log files that will be monitored");
		log2.setWrapStyleWord(true);
		log2.setLineWrap(true);
		log2.setEditable(false);
		log2.setCursor(null);
		log2.setOpaque(false);
		log2.setFocusable(false);
		log2.setBorder(null);
		log2.setFont(new Font("Arial", Font.PLAIN, 12));
		log2.setBackground(getBackground());
		log2.setMaximumSize(new Dimension(170, 25));
		log2.setPreferredSize(new Dimension(170, 25));
		JPanel p71 = new JPanel();
		p71.setBackground(Color.WHITE);
		p71.setLayout(new GridLayout());
		p71.setMaximumSize(new Dimension(700, 13));
		p71.setPreferredSize(new Dimension(700, 13));
		p71.add(log2);
		JPanel p72 = new JPanel();
		p72.setBackground(Color.WHITE);
		p72.setLayout(new BoxLayout(p72, BoxLayout.Y_AXIS));
		trunning = new JTextField();
		p72.add(addField(trunning, "Running: ", 0));
		tdebug = new JTextField();
		p72.add(addField(tdebug, "Debug: ", 1));
		tsummary = new JTextField();
		p72.add(addField(tsummary, "Summary: ", 2));
		tinfo = new JTextField();
		p72.add(addField(tinfo, "Info: ", 3));
		tcli = new JTextField();
		p72.add(addField(tcli, "Cli: ", 4));
		p7.add(p71);
		p7.add(p72);
		thardwareconfig = new JTextField();
		addPanel(
				"Hardware Config XML",
				"Location of the XML file that contains the devices configuration",
				thardwareconfig, Repository.REMOTEHARDWARECONFIGDIRECTORY, 535,
				true, null);
		ActionListener actionlistener = new ActionListener() {

			public void actionPerformed(ActionEvent ev) {
				if (!tname.getText().equals("")) {
					saveXML(false);
				} else {
					CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
							ConfigFiles.this, "Filename missing",
							"No file name given");
				}
			}
		};
		tname = new JTextField();
		addPanel("File name", "File name to store this configuration", tname,
				"", 944, true, actionlistener);
		tdbfile = new JTextField();
		addPanel("Database XML path",
				"File location for database configuration", tdbfile,
				Repository.REMOTEDATABASECONFIGPATH
						+ Repository.REMOTEDATABASECONFIGFILE, 604, true, null);
		temailfile = new JTextField();
		addPanel("Email XML path", "File location for email configuration",
				temailfile, Repository.REMOTEEMAILCONFIGPATH
						+ Repository.REMOTEEMAILCONFIGFILE, 672, true, null);
		tceport = new JTextField();
		addPanel("Central Engine Port", "Central Engine port", tceport,
				Repository.getCentralEnginePort(), 740, false, null);
		traPort = new JTextField();
		addPanel("Resource Allocator Port", "Resource Allocator Port", traPort,
				Repository.getResourceAllocatorPort(), 808, false, null);
		thttpPort = new JTextField();
		addPanel("HTTP Server Port", "HTTP Server Port", thttpPort,
				Repository.getHTTPServerPort(), 876, false, null);

		final JButton loadXML = new JButton("Load Config");
		loadXML.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent ev) {
				try {
					try {
						Repository.c.cd(Repository.USERHOME
								+ "/twister/config/");
					} catch (Exception e) {
						System.out
								.println("Could not get: /home/tscguest/twister/Config/");
					}
					int size = Repository.c.ls(
							Repository.USERHOME + "/twister/config/").size();
					ArrayList<String> temp = new ArrayList<String>();
					for (int i = 0; i < size; i++) {
						String name = ((LsEntry) Repository.c.ls(
								Repository.USERHOME + "/twister/config/")
								.get(i)).getFilename();
						if (name.split("\\.").length == 0) {
							continue;
						}
						if (name.indexOf(".xml") == -1) {
							continue;
						}
						temp.add(name);
					}
					String configs[] = new String[temp.size()];
					temp.toArray(configs);

					final String config;
					JComboBox combo = new JComboBox(configs);
					int resp = (Integer) CustomDialog.showDialog(combo,
							JOptionPane.INFORMATION_MESSAGE,
							JOptionPane.OK_CANCEL_OPTION, ConfigFiles.this,
							"Config", null);
					if (resp == JOptionPane.OK_OPTION) {
						config = combo.getSelectedItem().toString();
					} else {
						config = null;
					}
					if (config != null) {
						new Thread() {

							public void run() {
								setEnabledTabs(false);
								JFrame progress = new JFrame();
								progress.setAlwaysOnTop(true);
								progress.setLocation((int) loadXML
										.getLocationOnScreen().getX(),
										(int) loadXML.getLocationOnScreen()
												.getY());
								progress.setUndecorated(true);
								JProgressBar bar = new JProgressBar();
								bar.setIndeterminate(true);
								progress.add(bar);
								progress.pack();
								progress.setVisible(true);
								loadConfig(config);
								progress.dispose();
								setEnabledTabs(true);
							}
						}.start();
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
		loadXML.setBounds(760, 1020, 120, 20);
		paths.add(loadXML);
	}

	public void setEnabledTabs(boolean enable) {
		int nr = Repository.window.mainpanel.getTabCount();
		for (int i = 0; i < nr; i++) {
			if (i != 3) {
				Repository.window.mainpanel.setEnabledAt(i, enable);
			}
		}
	}

	public void loadConfig(String config) {
		try {
			InputStream in = null;
			try {
				in = Repository.c.get(config);
			} catch (Exception e) {
				System.out.println("Could not connect to " + config);
			}
			byte[] data = new byte[100];
			ByteArrayOutputStream buffer = new ByteArrayOutputStream();
			int nRead;
			try {
				while ((nRead = in.read(data, 0, data.length)) != -1) {
					buffer.write(data, 0, nRead);
				}
				buffer.flush();
			} catch (Exception e) {
				System.out.println("could not copy data from server " + config);
			}
			File theone = new File(Repository.temp + Repository.getBar()
					+ "Twister" + Repository.getBar() + "config"
					+ Repository.getBar() + config);
			FileOutputStream out = null;
			try {
				out = new FileOutputStream(Repository.temp
						+ Repository.getBar() + "Twister" + Repository.getBar()
						+ "config" + Repository.getBar() + config);
				buffer.writeTo(out);
				out.close();
				buffer.close();
				in.close();
			} catch (Exception e) {
				System.out.println("Could not write to " + Repository.temp
						+ Repository.getBar() + "Twister" + Repository.getBar()
						+ "config" + Repository.getBar() + config);
			}
			DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
			DocumentBuilder db = dbf.newDocumentBuilder();
			Document doc = null;
			try {
				doc = db.parse(theone);
			} catch (Exception e) {
				System.out.println(theone.getCanonicalPath()
						+ " is corrup or not a valid XML");
			}
			if (doc != null) {
				doc.getDocumentElement().normalize();
				NodeList nodeLst = doc.getElementsByTagName("FileType");
				if (nodeLst.getLength() > 0) {
					Node fstNode = nodeLst.item(0);
					Element fstElmnt = (Element) fstNode;
					NodeList fstNm = fstElmnt.getChildNodes();
					if (fstNm.item(0).getNodeValue().toString()
							.equals("config")) {
						in = new FileInputStream(theone);
						Repository.c.put(in, "fwmconfig.xml");
						in.close();
						Repository.emptyTestRepository();
						Repository.emptyLogs();
						File dir = new File(Repository.getUsersDirectory());
						String[] children = dir.list();
						for (int i = 0; i < children.length; i++) {
							new File(dir, children[i]).delete();
						}
						Repository.parseConfig();
						Repository.window.mainpanel.p2 = new Panel2(
								Repository.applet);
						Repository.window.mainpanel.setComponentAt(1,
								Repository.window.mainpanel.p2);
						Repository.window.mainpanel.p1.ep.refreshStructure();
						Repository.window.mainpanel.p4.getDBConfig().refresh();
						Repository.resetDBConf(
								Repository.REMOTEDATABASECONFIGFILE, true);
						Repository.resetEmailConf(
								Repository.REMOTEEMAILCONFIGFILE, true);
						tdbfile.setText(Repository.REMOTEDATABASECONFIGFILE);
						ttcpath.setText(Repository.TESTSUITEPATH);
						tMasterXML.setText(Repository.XMLREMOTEDIR);
						tUsers.setText(Repository.REMOTEUSERSDIRECTORY);
						tepid.setText(Repository.REMOTEEPIDDIR);
						tlog.setText(Repository.LOGSPATH);
						thardwareconfig
								.setText(Repository.REMOTEHARDWARECONFIGDIRECTORY);
						if (Repository.getLogs().size() > 0) {
							trunning.setText(Repository.getLogs().get(0));
						}
						trunning.setText(Repository.getLogs().get(0));
						tdebug.setText(Repository.getLogs().get(1));
						tsummary.setText(Repository.getLogs().get(2));
						tinfo.setText(Repository.getLogs().get(3));
						tcli.setText(Repository.getLogs().get(4));
						thardwareconfig
								.setText(Repository.REMOTEHARDWARECONFIGDIRECTORY);
						tdbfile.setText(Repository.REMOTEDATABASECONFIGPATH
								+ Repository.REMOTEDATABASECONFIGFILE);
						temailfile.setText(Repository.REMOTEEMAILCONFIGPATH
								+ Repository.REMOTEEMAILCONFIGFILE);
						thttpPort.setText(Repository.getHTTPServerPort());
						traPort.setText(Repository.getResourceAllocatorPort());
						tceport.setText(Repository.getCentralEnginePort());
					} else {
						CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
								ConfigFiles.this, "WARNING",
								"This is not a config file");
					}
				}
			} else {
				CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
						ConfigFiles.this, "WARNING",
						"Could not find Config tab");
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public JPanel addField(JTextField textfield, String text, int nr) {
		textfield.setMaximumSize(new Dimension(340, 25));
		textfield.setPreferredSize(new Dimension(340, 25));
		if (Repository.getLogs().size() > 0) {
			textfield.setText(Repository.getLogs().get(nr));
		}
		JLabel l1 = new JLabel(text);
		l1.setMaximumSize(new Dimension(65, 20));
		l1.setPreferredSize(new Dimension(65, 20));
		JPanel p721 = new JPanel();
		p721.setBackground(Color.WHITE);
		p721.add(l1);
		p721.add(textfield);
		p721.setMaximumSize(new Dimension(800, 28));
		p721.setPreferredSize(new Dimension(800, 28));
		return p721;
	}

	public void addPanel(String title, String description,
			final JTextField textfield, String fieldtext, int Y,
			boolean withbutton, ActionListener actionlistener) {
		JPanel p1 = new JPanel();
		p1.setBackground(Color.WHITE);
		TitledBorder border = BorderFactory.createTitledBorder(title);
		border.setTitleFont(new Font("Arial", Font.PLAIN, 14));
		border.setBorder(BorderFactory.createLineBorder(
				new Color(150, 150, 150), 1));
		p1.setBorder(border);
		p1.setLayout(new BoxLayout(p1, BoxLayout.Y_AXIS));
		p1.setBounds(80, Y, 800, 70);
		paths.add(p1);
		JTextArea tcpath = new JTextArea(description);
		tcpath.setWrapStyleWord(true);
		tcpath.setLineWrap(true);
		tcpath.setEditable(false);
		tcpath.setCursor(null);
		tcpath.setOpaque(false);
		tcpath.setFocusable(false);
		tcpath.setFont(new Font("Arial", Font.PLAIN, 12));
		tcpath.setBackground(getBackground());
		tcpath.setMaximumSize(new Dimension(170, 18));
		tcpath.setPreferredSize(new Dimension(170, 18));
		tcpath.setBorder(null);
		JPanel p11 = new JPanel();
		p11.setBackground(Color.WHITE);
		p11.setLayout(new GridLayout());
		p11.add(tcpath);
		p11.setMaximumSize(new Dimension(700, 13));
		p11.setPreferredSize(new Dimension(700, 13));
		textfield.setMaximumSize(new Dimension(340, 27));
		textfield.setPreferredSize(new Dimension(340, 27));
		textfield.setText(fieldtext);
		JButton b = null;
		if (withbutton) {
			b = new JButton("...");
			b.setMaximumSize(new Dimension(50, 20));
			b.setPreferredSize(new Dimension(50, 20));
			if (actionlistener == null) {
				b.addActionListener(new AbstractAction() {

					public void actionPerformed(ActionEvent ev) {
						if (fileChooser == null) {
							initializeFileBrowser();
						}
						try {
							RETURN_TYPE answer = fileChooser
									.showOpenDialog(ConfigFiles.this);
							if (answer == RETURN_TYPE.APPROVE) {
								FileObject aFileObject = fileChooser
										.getSelectedFile();
								String safeName = VFSUtils
										.getFriendlyName(aFileObject.toString());
								safeName = safeName.substring(safeName
										.indexOf(Repository.host)
										+ Repository.host.length());
								String[] check = safeName.split("/");
								if (check[check.length - 1]
										.equals(check[check.length - 2])) {
									StringBuffer buffer = new StringBuffer();
									for (int i = 0; i < check.length - 1; i++) {
										buffer.append(check[i] + "/");
									}
									safeName = buffer.toString();
								}
								textfield.setText(safeName);
							}
						} catch (Exception e) {
							fileChooser = null;
							e.printStackTrace();
						}
					}
				});
			} else {
				b.addActionListener(actionlistener);
				b.setText("Save");
				b.setMaximumSize(new Dimension(70, 20));
				b.setPreferredSize(new Dimension(70, 20));
			}
		}
		JPanel p12 = new JPanel();
		p12.setBackground(Color.WHITE);
		p12.add(textfield);
		if (withbutton) {
			p12.add(b);
		}
		p12.setMaximumSize(new Dimension(700, 32));
		p12.setPreferredSize(new Dimension(700, 32));
		p1.add(p11);
		p1.add(p12);
	}

	public static void saveXML(boolean blank) {
		boolean saved = true;
		try {
			DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory
					.newInstance();
			DocumentBuilder documentBuilder = documentBuilderFactory
					.newDocumentBuilder();
			Document document = documentBuilder.newDocument();
			TransformerFactory transformerFactory = TransformerFactory
					.newInstance();
			Transformer transformer = transformerFactory.newTransformer();
			transformer.setOutputProperty(OutputKeys.INDENT, "yes");
			transformer.setOutputProperty(
					"{http://xml.apache.org/xslt}indent-amount", "4");
			DOMSource source = new DOMSource(document);
			Comment simpleComment = document
					.createComment("\n Master config file for TSC.\n \n Logs Path: Where CE and PE write their getLogs(). Reports Path: Where all reports are saved.\n Test Suite Config: All info about the current Test Suite (Test Plan).\n");
			document.appendChild(simpleComment);
			Element root = document.createElement("Root");
			document.appendChild(root);
			Element rootElement = document.createElement("FileType");
			root.appendChild(rootElement);
			rootElement.appendChild(document.createTextNode("config"));
			addTag("CentralEnginePort", tceport.getText(), root, blank,
					document);
			addTag("ResourceAllocatorPort", traPort.getText(), root, blank,
					document);
			addTag("HttpServerPort", thttpPort.getText(), root, blank, document);
			addTag("TestCaseSourcePath", ttcpath.getText(), root, blank,
					document);
			addTag("MasterXMLTestSuite", tMasterXML.getText(), root, blank,
					document);
			addTag("UsersPath", tUsers.getText(), root, blank, document);
			addTag("LogsPath", tlog.getText(), root, blank, document);
			rootElement = document.createElement("LogFiles");
			root.appendChild(rootElement);
			addTag("logRunning", trunning.getText(), rootElement, blank,
					document);
			addTag("logDebug", tdebug.getText(), rootElement, blank, document);
			addTag("logSummary", tsummary.getText(), rootElement, blank,
					document);
			addTag("logTest", tinfo.getText(), rootElement, blank, document);
			addTag("logCli", tcli.getText(), rootElement, blank, document);
			addTag("DbConfigFile", tdbfile.getText(), root, blank, document);
			addTag("EPIdsFile", tepid.getText(), root, blank, document);
			addTag("HardwareConfig", thardwareconfig.getText(), root, blank,
					document);
			addTag("EmailConfigFile", temailfile.getText(), root, blank,
					document);
			String temp;
			if (blank) {
				temp = "fwmconfig";
			} else {
				temp = tname.getText();
			}
			File file = new File(Repository.temp + Repository.getBar()
					+ "Twister" + Repository.getBar() + temp + ".xml");
			Result result = new StreamResult(file);
			transformer.transform(source, result);
			Repository.c.cd(Repository.USERHOME + "/twister/config/");
			System.out.println("Saving to: " + Repository.USERHOME
					+ "/twister/config/");
			FileInputStream in = new FileInputStream(file);
			Repository.c.put(in, file.getName());
			in.close();
		} catch (ParserConfigurationException e) {
			System.out
					.println("DocumentBuilder cannot be created which satisfies the configuration requested");
			saved = false;
		} catch (TransformerConfigurationException e) {
			System.out.println("Could not create transformer");
			saved = false;
		} catch (Exception e) {
			e.printStackTrace();
			saved = false;
		}
		if (saved) {
			CustomDialog.showInfo(JOptionPane.INFORMATION_MESSAGE,
					Repository.window.mainpanel.p4.getConfig(), "Successfull",
					"File successfully saved");
		} else {
			CustomDialog.showInfo(JOptionPane.WARNING_MESSAGE,
					Repository.window.mainpanel.p4.getConfig(), "Warning",
					"File could not be saved ");
		}
	}

	public static void addTag(String tagname, String tagcontent, Element root,
			boolean blank, Document document) {
		Element rootElement = document.createElement(tagname);
		root.appendChild(rootElement);
		String temp;
		if (blank) {
			temp = "";
		} else {
			temp = tagcontent;
		}
		rootElement.appendChild(document.createTextNode(temp));
	}

	public void initializeFileBrowser() {
		fileChooser = new VFSJFileChooser("sftp://" + Repository.user + ":"
				+ Repository.password + "@" + Repository.host + "/home/"
				+ Repository.user + "/twister/config/");
		fileChooser.setFileHidingEnabled(true);
		fileChooser.setMultiSelectionEnabled(false);
		fileChooser
				.setFileSelectionMode(VFSJFileChooser.SELECTION_MODE.FILES_AND_DIRECTORIES);
	}
}
