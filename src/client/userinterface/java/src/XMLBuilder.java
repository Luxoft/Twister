/*
   File: XMLBuilder.java ; This file is part of Twister.

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

import java.util.ArrayList;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.Transformer;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.OutputKeys;
import java.io.File;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.Result;
import java.io.FileInputStream;

public class XMLBuilder {

	private DocumentBuilderFactory documentBuilderFactory;
	private Document document;
	private TransformerFactory transformerFactory;
	private Transformer transformer;
	private DOMSource source;
	private ArrayList<Item> suite;
	private boolean skip;
	private int id = 1000;

	public XMLBuilder(ArrayList<Item> suite) {
		try {
			documentBuilderFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder documentBuilder = documentBuilderFactory
					.newDocumentBuilder();
			document = documentBuilder.newDocument();
			transformerFactory = TransformerFactory.newInstance();
			transformer = transformerFactory.newTransformer();
			transformer.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION,
					"yes");
			transformer.setOutputProperty(OutputKeys.INDENT, "yes");
			transformer.setOutputProperty(
					"{http://xml.apache.org/xslt}indent-amount", "4");
			source = new DOMSource(document);
			this.suite = suite;
		} catch (ParserConfigurationException e) {
			System.out
					.println("DocumentBuilder cannot be created which satisfies the configuration requested");
		} catch (TransformerConfigurationException e) {
			System.out.println("Could not create transformer");
		}
	}

	public boolean getRunning(Item item) {
		if (item.getType() == 1) {
			if (item.getSubItem(0).getValue().equals("true")) {
				return true;
			} else {
				return false;
			}
		} else {
			int subitemsnr = item.getSubItemsNr();
			for (int i = 0; i < subitemsnr; i++) {
				if (getRunning(item.getSubItem(i))) {
					return true;
				}
			}
			return false;
		}
	}

	public void createXML(boolean skip) {
		this.skip = skip;
		Element root = document.createElement("Root");
		document.appendChild(root);
		int nrsuite = suite.size();
		for (int i = 0; i < nrsuite; i++) {
			int nrtc = suite.get(i).getSubItemsNr();
			boolean go = false;
			if (skip) {
				for (int j = 0; j < nrtc; j++) {
					if (getRunning(suite.get(i))) {
						go = true;
						break;
					}
				}
			}
			if (!go && skip) {
				continue;
			}
			Element rootElement = document.createElement("TestSuite");
			root.appendChild(rootElement);
			Element em2 = document.createElement("tsName");
			em2.appendChild(document.createTextNode(suite.get(i).getName()));
			rootElement.appendChild(em2);
			if (suite.get(i).getEpId() != null
					&& !suite.get(i).getEpId().equals("")) {
				Element EP = document.createElement("EpId");
				EP.appendChild(document.createTextNode(suite.get(i).getEpId()));
				rootElement.appendChild(EP);
			}
			for (int j = 0; j < suite.get(i).getUserDefNr(); j++) {
				Element userdef = document.createElement("UserDefined");
				Element pname = document.createElement("propName");
				pname.appendChild(document.createTextNode(suite.get(i)
						.getUserDef(j)[0]));
				userdef.appendChild(pname);
				Element pvalue = document.createElement("propValue");
				pvalue.appendChild(document.createTextNode(suite.get(i)
						.getUserDef(j)[1]));
				userdef.appendChild(pvalue);
				rootElement.appendChild(userdef);
			}
			for (int j = 0; j < nrtc; j++) {
				addSubElement(rootElement,
						Repository.getSuita(i).getSubItem(j), skip);
			}
		}
	}

	public void addSubElement(Element rootelement, Item item, boolean skip) {
		if (item.getType() == 0) {
			Element prop = document.createElement("Property");
			rootelement.appendChild(prop);
			Element em4 = document.createElement("propName");
			em4.appendChild(document.createTextNode(item.getName()));
			prop.appendChild(em4);
			Element em5 = document.createElement("propValue");
			em5.appendChild(document.createTextNode(item.getValue()));
			prop.appendChild(em5);
		} else if (item.getType() == 1) {
			if (item.getSubItem(0).getValue().equals("false") && skip) {
				return;
			}
			Element tc = document.createElement("TestCase");
			rootelement.appendChild(tc);
			Element em3 = document.createElement("tcName");
			em3.appendChild(document.createTextNode(Repository
					.getTestSuitePath() + item.getFileLocation()));
			tc.appendChild(em3);
			if (skip) {
				Element em6 = document.createElement("tcID");
				em6.appendChild(document.createTextNode(id + ""));
				id++;
				tc.appendChild(em6);
				Element em7 = document.createElement("Title");
				em7.appendChild(document.createTextNode(""));
				tc.appendChild(em7);
				Element em8 = document.createElement("Summary");
				em8.appendChild(document.createTextNode(""));
				tc.appendChild(em8);
				Element em9 = document.createElement("Priority");
				em9.appendChild(document.createTextNode("Medium"));
				tc.appendChild(em9);
				Element em10 = document.createElement("Dependancy");
				em10.appendChild(document.createTextNode(" "));
				tc.appendChild(em10);
			}
			Element prop = document.createElement("Property");
			tc.appendChild(prop);
			Element em4 = document.createElement("propName");
			em4.appendChild(document.createTextNode("Runnable"));
			prop.appendChild(em4);
			Element em5 = document.createElement("propValue");
			em5.appendChild(document.createTextNode(item.isRunnable() + ""));
			prop.appendChild(em5);
			int nrprop = item.getSubItemsNr();
			int k;
			if (skip) {
				k = 1;
			} else {
				k = 0;
			}
			for (; k < nrprop; k++) {
				addSubElement(tc, item.getSubItem(k), skip);
			}
		} else {
			int nrtc = item.getSubItemsNr();
			boolean go = false;
			if (skip) {
				for (int j = 0; j < nrtc; j++) {
					if (getRunning(item.getSubItem(j))) {
						go = true;
						break;
					}
				}
			}
			if (!go && skip) {
				return;
			}
			Element rootElement2 = document.createElement("TestSuite");
			rootelement.appendChild(rootElement2);
			Element em2 = document.createElement("tsName");
			em2.appendChild(document.createTextNode(item.getName()));
			rootElement2.appendChild(em2);
			if (item.getEpId() != null && !item.getEpId().equals("")) {
				Element EP = document.createElement("EpId");
				EP.appendChild(document.createTextNode(item.getEpId()));
				rootElement2.appendChild(EP);
			}
			for (int i = 0; i < item.getSubItemsNr(); i++) {
				addSubElement(rootElement2, item.getSubItem(i), skip);
			}
		}
	}

	public void printXML() {
		StreamResult result = new StreamResult(System.out);
		try {
			transformer.transform(source, result);
		} catch (Exception e) {
			System.out.println("Could not write standard output stream");
		}
	}

	public void writeXMLFile(String filename, boolean local) {
		File file = new File(filename);
		Result result = new StreamResult(file);
		try {
			transformer.transform(source, result);
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("Could not write to file");
		}
		if (!local) {
			try {
				if (skip) {
					String dir = Repository.getXMLRemoteDir();
					String[] path = dir.split("/");
					StringBuffer result2 = new StringBuffer();
					if (path.length > 0) {
						for (int i = 0; i < path.length - 1; i++) {
							result2.append(path[i]);
							result2.append("/");
						}
					}
					Repository.c.cd(result2.toString());
					FileInputStream in = new FileInputStream(file);
					Repository.c.put(in, file.getName());
					in.close();
				} else {
					Repository.c.cd(Repository.getRemoteUsersDirectory());
					FileInputStream in = new FileInputStream(file);
					Repository.c.put(in, file.getName());
					in.close();
				}
			} catch (Exception e) {
				e.printStackTrace();
				System.out.println("Could not get XML file to upload on sever");
			}
		}
	}
}
