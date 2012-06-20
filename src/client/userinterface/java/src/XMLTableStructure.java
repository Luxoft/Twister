/*
File: XMLTableStructure.java ; This file is part of Twister.

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
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.SAXException;
import java.io.IOException;
import java.awt.Graphics;
import java.awt.FontMetrics;
import java.awt.Font;
import java.util.ArrayList;
import java.io.InputStream;

public class XMLTableStructure {

	private DocumentBuilderFactory dbf;
	private DocumentBuilder db;
	private Document doc;
	private Node fstNode, secNode, trdNode;
	private Element fstElmnt, fstNmElmnt, secElmnt, secNmElmnt, trdElmnt,
			trdNmElmnt;
	private NodeList fstNmElmntLst, fstNm, fstNmElmntLst2, secNmElmntLst,
			secNm, secNmElmntLst2, trdNmElmntLst, trdNm, trdNmElmntLst2,
			trdNm2;
	private File f;
	private String name, value;
	private ArrayList<Integer> editable = new ArrayList<Integer>();
	private ArrayList<String> columns = new ArrayList<String>();

	public XMLTableStructure(InputStream in) {
		dbf = DocumentBuilderFactory.newInstance();
		try {
			db = dbf.newDocumentBuilder();
			doc = db.parse(in);
			doc.getDocumentElement().normalize();
			in.close();
		} catch (ParserConfigurationException e) {
			try {
				in.close();
			} catch (Exception ex) {
				ex.printStackTrace();
			}
			System.out.println("Could not create a XML parser configuration");
		} catch (SAXException e) {
			try {
				in.close();
			} catch (Exception ex) {
				ex.printStackTrace();
			}
			System.out.println("The document is empty or not valid");
		} catch (IOException e) {
			try {
				in.close();
			} catch (Exception ex) {
				ex.printStackTrace();
			}
			System.out.println("Could not read the document");
		} catch (Exception e) {
			try {
				in.close();
			} catch (Exception ex) {
				ex.printStackTrace();
			}
			e.printStackTrace();
		}
	}

	public ArrayList<String> parseXML() {
		NodeList nodeLst = doc.getElementsByTagName("Column");
		if (nodeLst.getLength() == 0) {
			System.out.println("Table structure document has no Column tags");
		}
		for (int s = 0; s < nodeLst.getLength(); s++) {
			fstNode = nodeLst.item(s);
			fstElmnt = (Element) fstNode;
			fstNmElmntLst = fstElmnt.getElementsByTagName("Name");
			fstNmElmnt = (Element) fstNmElmntLst.item(0);
			fstNm = fstNmElmnt.getChildNodes();
			columns.add(fstNm.item(0).getNodeValue().toString());
			fstNmElmntLst = fstElmnt.getElementsByTagName("Editable");
			if (fstNmElmntLst.getLength() == 1) {
				editable.add(columns.size() - 1);
			}
		}
		return columns;
	}

	public ArrayList<Integer> getEditableColumns() {
		return editable;
	}
}
