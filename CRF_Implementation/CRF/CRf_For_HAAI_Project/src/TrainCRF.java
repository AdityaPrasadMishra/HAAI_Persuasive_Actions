import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.regex.Pattern;

import cc.mallet.fst.CRF;
import cc.mallet.fst.CRFOptimizableByLabelLikelihood;
import cc.mallet.fst.CRFTrainerByValueGradients;
import cc.mallet.fst.CRFWriter;
import cc.mallet.fst.MultiSegmentationEvaluator;
import cc.mallet.fst.TransducerEvaluator;
import cc.mallet.fst.TransducerTrainer;
import cc.mallet.optimize.Optimizable;
import cc.mallet.pipe.CharSequence2TokenSequence;
import cc.mallet.pipe.FeatureSequence2FeatureVector;
import cc.mallet.pipe.Input2CharSequence;
import cc.mallet.pipe.Pipe;
import cc.mallet.pipe.PrintInputAndTarget;
import cc.mallet.pipe.SerialPipes;
import cc.mallet.pipe.Target2Label;
import cc.mallet.pipe.TokenSequence2FeatureSequence;
import cc.mallet.pipe.TokenSequenceLowercase;
import cc.mallet.pipe.TokenSequenceRemoveStopwords;
import cc.mallet.pipe.iterator.FileIterator;
import cc.mallet.types.InstanceList;

public class TrainCRF {
	
	
	 public void run (InstanceList trainingData, InstanceList testingData) {
	      // setup:
	      //    CRF (model) and the state machine
	      //    CRFOptimizableBy* objects (terms in the objective function)
	      //    CRF trainer
	      //    evaluator and writer

	      // model
	      CRF crf = new CRF(trainingData.getDataAlphabet(),
	                        trainingData.getTargetAlphabet());
	      // construct the finite state machine
	      crf.addFullyConnectedStatesForLabels();
	      // initialize model's weights
	      crf.setWeightsDimensionAsIn(trainingData, false);

	      //  CRFOptimizableBy* objects (terms in the objective function)
	      // objective 1: label likelihood objective
	      CRFOptimizableByLabelLikelihood optLabel =
	          new CRFOptimizableByLabelLikelihood(crf, trainingData);

	      // CRF trainer
	      Optimizable.ByGradientValue[] opts =
	          new Optimizable.ByGradientValue[]{optLabel};
	      // by default, use L-BFGS as the optimizer
	      CRFTrainerByValueGradients crfTrainer =
	          new CRFTrainerByValueGradients(crf, opts);

	      // *Note*: labels can also be obtained from the target alphabet
	      String[] labels = new String[]{"I-PER", "I-LOC", "I-ORG", "I-MISC"};
	      TransducerEvaluator evaluator = new MultiSegmentationEvaluator(
	          new InstanceList[]{trainingData, testingData},
	          new String[]{"train", "test"}, labels, labels) {
	        @Override
	        public boolean precondition(TransducerTrainer tt) {
	          // evaluate model every 5 training iterations
	          return tt.getIteration() % 5 == 0;
	        }
	      };
	      crfTrainer.addEvaluator(evaluator);

	      CRFWriter crfWriter = new CRFWriter("ner_crf.model") {
	        @Override
	        public boolean precondition(TransducerTrainer tt) {
	          // save the trained model after training finishes
	          return tt.getIteration() % Integer.MAX_VALUE == 0;
	        }
	      };
	      crfTrainer.addEvaluator(crfWriter);

	      // all setup done, train until convergence
	      crfTrainer.setMaxResets(0);
	      crfTrainer.train(trainingData, Integer.MAX_VALUE);
	      // evaluate
	      evaluator.evaluate(crfTrainer);

	      // save the trained model (if CRFWriter is not used)
	      // FileOutputStream fos = new FileOutputStream("ner_crf.model");
	      // ObjectOutputStream oos = new ObjectOutputStream(fos);
	      // oos.writeObject(crf);
	    }
	 	
	 	Pipe pipe;

	    public TrainCRF() {
	        pipe = buildPipe();
	    }

	    public Pipe buildPipe() {
	        ArrayList pipeList = new ArrayList();

	        // Read data from File objects
	        pipeList.add(new Input2CharSequence("UTF-8"));

	        // Regular expression for what constitutes a token.
	        //  This pattern includes Unicode letters, Unicode numbers, 
	        //   and the underscore character. Alternatives:
	        //    "\\S+"   (anything not whitespace)
	        //    "\\w+"    ( A-Z, a-z, 0-9, _ )
	        //    "[\\p{L}\\p{N}_]+|[\\p{P}]+"   (a group of only letters and numbers OR
	        //                                    a group of only punctuation marks)
	        Pattern tokenPattern =
	            Pattern.compile("[\\p{L}\\p{N}_]+");

	        // Tokenize raw strings
	        pipeList.add(new CharSequence2TokenSequence(tokenPattern));

	        // Normalize all tokens to all lowercase
	        pipeList.add(new TokenSequenceLowercase());

	        // Remove stopwords from a standard English stoplist.
	        //  options: [case sensitive] [mark deletions]
	        pipeList.add(new TokenSequenceRemoveStopwords(false, false));

	        // Rather than storing tokens as strings, convert 
	        //  them to integers by looking them up in an alphabet.
	        pipeList.add(new TokenSequence2FeatureSequence());

	        // Do the same thing for the "target" field: 
	        //  convert a class label string to a Label object,
	        //  which has an index in a Label alphabet.
	        pipeList.add(new Target2Label());

	        // Now convert the sequence of features to a sparse vector,
	        //  mapping feature IDs to counts.
	        pipeList.add(new FeatureSequence2FeatureVector());

	        // Print out the features and the label
	        pipeList.add(new PrintInputAndTarget());

	        return new SerialPipes(pipeList);
	    }

	    public InstanceList readDirectory(File directory) {
	        return readDirectories(new File[] {directory});
	    }

	    public InstanceList readDirectories(File[] directories) {
	        
	        // Construct a file iterator, starting with the 
	        //  specified directories, and recursing through subdirectories.
	        // The second argument specifies a FileFilter to use to select
	        //  files within a directory.
	        // The third argument is a Pattern that is applied to the 
	        //   filename to produce a class label. In this case, I've 
	        //   asked it to use the last directory name in the path.
	        FileIterator iterator =
	            new FileIterator(directories,
	                             new TxtFilter(),
	                             FileIterator.LAST_DIRECTORY);

	        // Construct a new instance list, passing it the pipe
	        //  we want to use to process instances.
	        InstanceList instances = new InstanceList(pipe);

	        // Now process each instance provided by the iterator.
	        instances.addThruPipe(iterator);

	        return instances;
	    }

	    public static void main (String[] args) throws IOException {

	        TrainCRF trainer = new TrainCRF();
	        InstanceList instances = trainer.readDirectory(new File(args[0]));
	        instances.save(new File(args[1]));

	    }

	    /** This class illustrates how to build a simple file filter */
	    class TxtFilter implements FileFilter {

	        /** Test whether the string representation of the file 
	         *   ends with the correct extension. Note that {@ref FileIterator}
	         *   will only call this filter if the file is not a directory,
	         *   so we do not need to test that it is a file.
	         */
	        public boolean accept(File file) {
	            return file.toString().endsWith(".txt");
	        }
	    }


}
