/*
* SnowmanPlayer is a class that plays the game Snowman.
* The Algorithm is described as follows: 
	* 0. clear frequency
	* 1. wrong letter guess -> remove all words with that letter
	* 2. right letter guess -> check for pattern
	* 3. pattern doesn't match -> remove word from Set
	* 4. pattern match -> check for occurence of letter
	* 5. word doesn't have same occurence -> remove word
	* 6. word has same occurence -> get frequency
		* (repeating letters in word will have a frequency of 1) ^ (letters that dont appear in wordlist get freq of zero) 
		* ^ (previous guessed letters get frequency of zero)
	* 7. guess the letter based on max frequency
	* 8. if the size of wordlist is 1 then return the non guessed letters (ie. wherever you see a "*" a letter for that will be guessed)

* Faroq A. Khan
* @version 1.0
* November 24th 2017
*/

import java.util.*;

public class SnowmanPlayer
{
	// static data structures
	static String[] clone_words;
	static HashSet<String> hs_words = new HashSet<String>();
	static List<String> found = new ArrayList<String>();
	static List<String> word_arr = new ArrayList<String>();
	static HashSet<String> g_words = new HashSet<String>(); 
	static int[] freq = new int[26];

	//@return user name in lastName, FirstName format
	public static String getAuthor(){return "Khan, Farooq";}

	/*
	* @params words[]: array of words to guess from
	* @params minLength: smallest number of length a word can be
	* @params maxLength: largest number of length a word can be
	* @params allowedChars: only these characters can be guessed
	*/
	public static void startGame(String[] words, int minLength, int maxLength, String allowedChars)
	{
		// clone words array so it can be used by startNewWord method

		clone_words = words.clone(); 
	}

	/*
	* @params length: gives the length of the secretWord
	*/
	public static void startNewWord(int length)
	{
		// clear the HashSet and arrays from previous word
		hs_words.clear();
		found.clear();
		for (int i=0; i<26; i++){freq[i] = 0;}

		int clone_words_len = clone_words.length; // lenght of words array
		for (int i=0; i<clone_words_len; i++) // iterate over list of possible words
		{
			String clone_word = clone_words[i]; 
			int clone_word_len = clone_word.length(); 

			// add the words that have same length as secret word
			if (clone_word_len == length) {hs_words.add(clone_word); continue;}
		} 			
	}	

	/*
	* @params pattern: shows a string of correct guessedLetters and the not yet guessed letters
	* @params previousGuesses: shows a string of the guesses that have been made
	* @reeturn char: return the letter that will be guessed
	*/
	public static char guessLetter(String pattern, String previousGuesses)
	{

		// clear frequency at start of each guess
		for (int i=0; i<26; i++) {freq[i]=0;}
		
		// -----------------------------------------------------------------------------------------
		// ------------------------- check patter for repeated characters --------------------------
		// -----------------------------------------------------------------------------------------

		// counter for occurences of characters in pattern
		int[] letter_repetition_pattern = new int[26]; 
		
		for (int i=0; i<pattern.length(); i++)
		{
			if (pattern.charAt(i) != '*')
			{
				int pat_rep_char = (int) (pattern.charAt(i)) - 97; 
				letter_repetition_pattern[pat_rep_char]++; 
			}
		}
		// -----------------------------------------------------------------------------------------
		// ------------------------- check for repeated characters in words ------------------------
		// -----------------------------------------------------------------------------------------
		Iterator<String> it = hs_words.iterator(); 
		while(it.hasNext())
		{
			String word = it.next(); // word that needs analyzing
			int word_len = word.length(); // length of that word

			int[] letter_repetition_word = new int[26]; // counter for occurences of characters in word
			for (int i=0; i<word_len; i++)
			{
				int word_rep_char = (int) (word.charAt(i)) - 97; 
				letter_repetition_word[word_rep_char]++; 
			}

			// checking of the current word is the one we want
			for (int i=0; i<word_len; i++)
			{
				// helper variables
				char pat_char = pattern.charAt(i);  // character of secrect word
				char word_char = word.charAt(i);    // character of plassable word
				int pat_int = (int)(pat_char)-97;   // index of character of secrect word
				int word_int = (int)(word_char)-97; // idex of character of plassable word  

				//  check if characters are the same and if they have the same number of occurences
				if (pat_char!='*' && (pat_char!=word_char || letter_repetition_pattern[pat_int] != letter_repetition_word[word_int]))
				{ found.add(word); }
			}

			// reset letter_repetition_word to zero
			for (int i=0; i<letter_repetition_word.length; i++) { letter_repetition_word[i] = 0; }
		}

		// reset letter_repetition_patter to zero
		for (int i=0; i<letter_repetition_pattern.length; i++) { letter_repetition_pattern[i] = 0; }

		// -----------------------------------------------------------------------------------------
		// ---------------------------- check if previousGuess was wrong ---------------------------
		// -----------------------------------------------------------------------------------------
		if (previousGuesses.length()>0)
		{
			// helper varaibles
			int prev_guess_len = previousGuesses.length()-1; // index of last guessed char
			char prev_guess_char = previousGuesses.charAt(prev_guess_len); // value of char
			boolean wrong_guess = true; // checker for accurate prev guess
			int pat_len = pattern.length(); // length of pattern length

			for (int i=0; i<pat_len; i++)
			{
				if (pattern.charAt(i) != '*' && prev_guess_char == pattern.charAt(i))
				{
					wrong_guess = false; // if we see a char that is same then our guess was right
					break; 
				}
			}
			
			// -----------------------------------------------------------------------------------------
			// ---------------------------- wrong guess -> remove word with that letter ----------------
			// -----------------------------------------------------------------------------------------

			if (wrong_guess)
			{
				Iterator<String> iterate_wrong_guess = hs_words.iterator(); 
				while (iterate_wrong_guess.hasNext()) // iterate over all words
				{
					String word = iterate_wrong_guess.next(); 
					int word_len = word.length(); 

					for (int i=0; i<word_len; i++) // iterate over all characters
					{
						if (prev_guess_char == word.charAt(i))
						{
							found.add(word); 
							continue; 
						}
					}
				}
			}
		}

		// -----------------------------------------------------------------------------------------
		// ------------------------------------ removing words ------------------------------------
		// -----------------------------------------------------------------------------------------
		Iterator<String> iter = found.iterator(); 
		while(iter.hasNext())
		{
			String word = iter.next(); 
			hs_words.remove(word); 
		}
			int len = 0; 
		// -----------------------------------------------------------------------------------------
		// ----------------------------------- evaluate frequency ----------------------------------
		// -----------------------------------------------------------------------------------------
		Iterator<String> iterate = hs_words.iterator(); 
		while(iterate.hasNext())
		{
			String word = iterate.next(); 
			int word_len = word.length(); 
			len = word_len; 
			boolean[] no_repeated_letters = new boolean[26]; 

			for (int i=0; i<26; i++) { no_repeated_letters[i] = false; } // initialze array

			// check for repeated letters
			for (int i=0; i<word_len; i++)
			{
				for (char j='a'; j<='z'; j++)
				{
					if (word.charAt(i) == j)
					{
						int ind = (int)(j) - 97; 
						no_repeated_letters[ind] = true; 
					}
				}
			}

			// add to frequency counter when characters match
			for(int i=0; i<word_len; i++)
			{
				for (char j='a'; j<='z'; j++)
				{
					int boo_ind = (int)(j) - 97; 
					if (word.charAt(i) == j && no_repeated_letters[boo_ind]) // && pattern.charAt(i) == '*')
					{
						freq[boo_ind]++; // increase frequency if characters match
						continue; 						
					}
				}
			}
		}
		// -----------------------------------------------------------------------------------------
		// ------------------------------ set frequency of useless chars to 0 ----------------------
		// -----------------------------------------------------------------------------------------

		// first get a boolean array that has false values for all the letters
		boolean[] letters = new boolean[26]; 
		for (int i=0; i<letters.length; i++) { letters[i] = false; }

		Iterator<String> fq_it = hs_words.iterator(); 
		while(fq_it.hasNext())
		{
			String fq_word = fq_it.next(); 
			for (int i=0; i<fq_word.length(); i++)
			{
				for (char j='a'; j<='z'; j++)
				{
					if (j == fq_word.charAt(i))
					{
						int fq_ind = (int)(j) - 97; 
						letters[fq_ind] = true; 
						continue; 
					}
				}
			}
		}
		
		// set the frequency of the letters that are not in the hs_words to zero
		for (int i=0; i<26; i++)
		{ if (letters[i] == false) { freq[i] = 0; } }

		// set the frequency of the letters to zero if already guessed
		for (int i=0; i<previousGuesses.length(); i++)
		{
			int id = (int)(previousGuesses.charAt(i)) - 97; 
			freq[id] = 0; 
		}

		// -----------------------------------------------------------------------------------------
		// ------------------------------ guess char -----------------------------------------------
		// -----------------------------------------------------------------------------------------

		// get the max character and set it to zero so that it cant be used again in the round
		int max = freq[0]; 
		int index = 0; 

		for (int i=0; i<26; i++)
		{
			if (max < freq[i])
			{
				max = freq[i]; 
				index = i; 
			}
		}
		if (len == 5 && hs_words.size()<=20)
		{
			System.out.println(" size: " + hs_words.size()); 
			System.out.println(" set: " + hs_words); 
		}

		char max_char = (char) (index+97); // gets the char with most occurences
		// if size is 1 then return the non gussed letters
		if (hs_words.size() == 1)
		{
			Iterator<String> s1_iter = hs_words.iterator(); 
			while(s1_iter.hasNext())
			{
				String word = s1_iter.next(); 
				int word_len = word.length(); 
				
				for(int i=0; i<word_len; i++)
				{ if (pattern.charAt(i) == '*') { return word.charAt(i); } }	
			}	
		}
		return max_char; 
	}

}