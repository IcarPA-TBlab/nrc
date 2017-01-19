package root.nrc_workspace.src;

import java.io.IOException;

import moss.Miner;


public class FeatureMaker {

	public FeatureMaker() {
	}
	
	
	private void runMoss(String path,String inputFile, int maxSupport, int minSupport) {
		
		String[] boo= new String[]{"-m"+minSupport,"-n"+maxSupport,"-inel",inputFile,"-onel",path+"/out.nel","-fsln",path+"/out.sln"};
		
		
		Miner moss= new Miner();
		try {
			moss.init(boo);
			
			moss.run();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	

	
	
	public static void main(String[] args) {
		
		//String inputFile= "/home/giacalone/ncRNA/dataset_test/merged.nel";
		
		String path=args[0];
		String inputFile=args[1];
		
		//String max=args[1]
		//String min=args[2]
		
		int maxSupport= Integer.parseInt(args[2]);
		int minSupport= Integer.parseInt(args[3]);
		
		
		
		new FeatureMaker().runMoss(path,inputFile,maxSupport,minSupport);
	}


}
