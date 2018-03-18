import re

from collections import defaultdict

PUTCTUATION = ['\, ', '\. ', '\! ', '\? ', '; ', '\n']

#stop word list from SMART (Salton,1971).  Available at ftp://ftp.cs.cornell.edu/pub/smart/english.stop
COMMON_STOP_WORDS = [
    "a", "a\\'s", "able", "about", "above", "according", "accordingly", "across", "actually", "afte", "afterwards", "again", "against", "ain\\'t", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "anothe", "any", "anybody", "anyhow", "anyone", "anything", "anyway", "anyways", "anywhere", "apart", "appea", "appreciate", "appropriate", "are", "aren\\'t", "around", "as", "aside", "ask", "asking", "associated", "at", "available", "away", "awfully", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "behind", "being", "believe", "below", "beside", "besides", "best", "bette", "between", "beyond", "both", "brief", "but", "by", "c\\'mon", "c\\'s", "came", "can", "can\\'t", "cannot", "cant", "cause", "causes", "certain", "certainly", "changes", "clearly", "co", "com", "come", "comes", "concerning", "consequently", "conside", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn\\'t", "course", "currently", "d", "definitely", "described", "despite", "did", "didn\\'t", "different", "do", "does", "doesn\\'t", "doing", "don\\'t", "done", "down", "downwards", "during", "each", "edu", "eg", "eight", "eithe", "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even", "eve", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "fa", "few", "fifth", "first", "five", "followed", "following", "follows", "fo", "forme", "formerly", "forth", "fou", "from", "furthe", "furthermore", "get", "gets", "getting", "given", "gives", "go", "goes", "going", "gone", "got", "gotten", "greetings", "had", "hadn\\'t", "happens", "hardly", "has", "hasn\\'t", "have", "haven\\'t", "having", "he", "he\\'s", "hello", "help", "hence", "he", "here", "here\\'s", "hereafte", "hereby", "herein", "hereupon", "hers", "herself", "hi", "him", "himself", "his", "hithe", "hopefully", "how", "howbeit", "howeve", "i\\'d", "i\\'ll", "i\\'m", "i\\'ve", "ie", "if", "ignored", "immediate", "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inne", "insofa", "instead", "into", "inward", "is", "isn\\'t", "it", "it\\'d", "it\\'ll", "it\\'s", "its", "itself", "just", "keep", "keeps", "kept", "know", "knows", "known", "last", "lately", "late", "latte", "latterly", "least", "less", "lest", "let", "let\\'s", "like", "liked", "likely", "little", "look", "looking", "looks", "ltd", "mainly", "many", "may", "maybe", "me", "mean", "meanwhile", "merely", "might", "more", "moreove", "most", "mostly", "much", "must", "my", "myself", "name", "namely", "nd", "nea", "nearly", "necessary", "need", "needs", "neithe", "neve", "nevertheless", "new", "next", "nine", "no", "nobody", "non", "none", "noone", "no", "normally", "not", "nothing", "novel", "now", "nowhere", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "othe", "others", "otherwise", "ought", "ou", "ours", "ourselves", "out", "outside", "ove", "overall", "own", "particula", "particularly", "pe", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", "provides", "que", "quite", "qv", "", "rathe", "rd", "re", "really", "reasonably", "regarding", "regardless", "regards", "relatively", "respectively", "right", "said", "same", "saw", "say", "saying", "says", "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "shall", "she", "should", "shouldn\\'t", "since", "six", "so", "some", "somebody", "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify", "specifying", "still", "sub", "such", "sup", "sure", "t\\'s", "take", "taken", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that\\'s", "thats", "the", "thei", "theirs", "them", "themselves", "then", "thence", "there", "there\\'s", "thereafte", "thereby", "therefore", "therein", "theres", "thereupon", "these", "they", "they\\'d", "they\\'ll", "they\\'re", "they\\'ve", "think", "third", "this", "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "togethe", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "twice", "two", "un", "unde", "unfortunately", "unless", "unlikely", "until", "unto", "up", "upon", "us", "use", "used", "useful", "uses", "using", "usually", "uucp", "value", "various", "very", "via", "viz", "vs", "want", "wants", "was", "wasn\\'t", "way", "we", "we\\'d", "we\\'ll", "we\\'re", "we\\'ve", "welcome", "well", "went", "were", "weren\\'t", "what", "what\\'s", "whateve", "when", "whence", "wheneve", "where", "where\\'s", "whereafte", "whereas", "whereby", "wherein", "whereupon", "whereve", "whethe", "which", "while", "whithe", "who", "who\\'s", "whoeve", "whole", "whom", "whose", "why", "will", "willing", "wish", "with", "within", "without", "won\\'t", "wonde", "would", "would", "wouldn\\'t", "yes", "yet", "you", "you\\'d", "you\\'ll", "you\\'re", "you\\'ve", "you", "yours", "yourself", "yourselves", "zero", ]
PADDED_COMMON_STOP_WORDS = [
    " a ", " a\\'s ", " able ", " about ", " above ", " according ", " accordingly ", " across ", " actually ", " afte ", " afterwards ", " again ", " against ", " ain\\'t ", " all ", " allow ", " allows ", " almost ", " alone ", " along ", " already ", " also ", " although ", " always ", " am ", " among ", " amongst ", " an ", " and ", " anothe ", " any ", " anybody ", " anyhow ", " anyone ", " anything ", " anyway ", " anyways ", " anywhere ", " apart ", " appea ", " appreciate ", " appropriate ", " are ", " aren\\'t ", " around ", " as ", " aside ", " ask ", " asking ", " associated ", " at ", " available ", " away ", " awfully ", " be ", " became ", " because ", " become ", " becomes ", " becoming ", " been ", " before ", " beforehand ", " behind ", " being ", " believe ", " below ", " beside ", " besides ", " best ", " bette ", " between ", " beyond ", " both ", " brief ", " but ", " by ", " c\\'mon ", " c\\'s ", " came ", " can ", " can\\'t ", " cannot ", " cant ", " cause ", " causes ", " certain ", " certainly ", " changes ", " clearly ", " co ", " com ", " come ", " comes ", " concerning ", " consequently ", " conside ", " considering ", " contain ", " containing ", " contains ", " corresponding ", " could ", " couldn\\'t ", " course ", " currently ", " definitely ", " described ", " despite ", " did ", " didn\\'t ", " different ", " do ", " does ", " doesn\\'t ", " doing ", " don\\'t ", " done ", " down ", " downwards ", " during ", " each ", " edu ", " eg ", " eight ", " eithe ", " else ", " elsewhere ", " enough ", " entirely ", " especially ", " et ", " etc ", " even ", " eve ", " every ", " everybody ", " everyone ", " everything ", " everywhere ", " ex ", " exactly ", " example ", " except ", " fa ", " few ", " fifth ", " first ", " five ", " followed ", " following ", " follows ", " fo ", " forme ", " formerly ", " forth ", " fou ", " from ", " furthe ", " furthermore ", " get ", " gets ", " getting ", " given ", " gives ", " go ", " goes ", " going ", " gone ", " got ", " gotten ", " greetings ", " had ", " hadn\\'t ", " happens ", " hardly ", " has ", " hasn\\'t ", " have ", " haven\\'t ", " having ", " he ", " he\\'s ", " hello ", " help ", " hence ", " he ", " here ", " here\\'s ", " hereafte ", " hereby ", " herein ", " hereupon ", " hers ", " herself ", " hi ", " him ", " himself ", " his ", " hithe ", " hopefully ", " how ", " howbeit ", " howeve ", " i\\'d ", " i\\'ll ", " i\\'m ", " i\\'ve ", " ie ", " if ", " ignored ", " immediate ", " in ", " inasmuch ", " inc ", " indeed ", " indicate ", " indicated ", " indicates ", " inne ", " insofa ", " instead ", " into ", " inward ", " is ", " isn\\'t ", " it ", " it\\'d ", " it\\'ll ", " it\\'s ", " its ", " itself ", " just ", " keep ", " keeps ", " kept ", " know ", " knows ", " known ", " last ", " lately ", " late ", " latte ", " latterly ", " least ", " less ", " lest ", " let ", " let\\'s ", " like ", " liked ", " likely ", " little ", " look ", " looking ", " looks ", " ltd ", " mainly ", " many ", " may ", " maybe ", " me ", " mean ", " meanwhile ", " merely ", " might ", " more ", " moreove ", " most ", " mostly ", " much ", " must ", " my ", " myself ", " name ", " namely ", " nd ", " nea ", " nearly ", " necessary ", " need ", " needs ", " neithe ", " neve ", " nevertheless ", " new ", " next ", " nine ", " no ", " nobody ", " non ", " none ", " noone ", " no ", " normally ", " not ", " nothing ", " novel ", " now ", " nowhere ", " obviously ", " of ", " off ", " often ", " oh ", " ok ", " okay ", " old ", " on ", " once ", " one ", " ones ", " only ", " onto ", " othe ", " others ", " otherwise ", " ought ", " ou ", " ours ", " ourselves ", " out ", " outside ", " ove ", " overall ", " own ", " particula ", " particularly ", " pe ", " perhaps ", " placed ", " please ", " plus ", " possible ", " presumably ", " probably ", " provides ", " que ", " quite ", " qv ", "  ", " rathe ", " rd ", " re ", " really ", " reasonably ", " regarding ", " regardless ", " regards ", " relatively ", " respectively ", " right ", " said ", " same ", " saw ", " say ", " saying ", " says ", " second ", " secondly ", " see ", " seeing ", " seem ", " seemed ", " seeming ", " seems ", " seen ", " self ", " selves ", " sensible ", " sent ", " serious ", " seriously ", " seven ", " several ", " shall ", " she ", " should ", " shouldn\\'t ", " since ", " six ", " so ", " some ", " somebody ", " somehow ", " someone ", " something ", " sometime ", " sometimes ", " somewhat ", " somewhere ", " soon ", " sorry ", " specified ", " specify ", " specifying ", " still ", " sub ", " such ", " sup ", " sure ", " t\\'s ", " take ", " taken ", " tell ", " tends ", " th ", " than ", " thank ", " thanks ", " thanx ", " that ", " that\\'s ", " thats ", " the ", " thei ", " theirs ", " them ", " themselves ", " then ", " thence ", " there ", " there\\'s ", " thereafte ", " thereby ", " therefore ", " therein ", " theres ", " thereupon ", " these ", " they ", " they\\'d ", " they\\'ll ", " they\\'re ", " they\\'ve ", " think ", " third ", " this ", " thorough ", " thoroughly ", " those ", " though ", " three ", " through ", " throughout ", " thru ", " thus ", " to ", " togethe ", " too ", " took ", " toward ", " towards ", " tried ", " tries ", " truly ", " try ", " trying ", " twice ", " two ", " un ", " unde ", " unfortunately ", " unless ", " unlikely ", " until ", " unto ", " up ", " upon ", " us ", " use ", " used ", " useful ", " uses ", " using ", " usually ", " uucp ", " value ", " various ", " very ", " via ", " viz ", " vs ", " want ", " wants ", " was ", " wasn\\'t ", " way ", " we ", " we\\'d ", " we\\'ll ", " we\\'re ", " we\\'ve ", " welcome ", " well ", " went ", " were ", " weren\\'t ", " what ", " what\\'s ", " whateve ", " when ", " whence ", " wheneve ", " where ", " where\\'s ", " whereafte ", " whereas ", " whereby ", " wherein ", " whereupon ", " whereve ", " whethe ", " which ", " while ", " whithe ", " who ", " who\\'s ", " whoeve ", " whole ", " whom ", " whose ", " why ", " will ", " willing ", " wish ", " with ", " within ", " without ", " won\\'t ", " wonde ", " would ", " would ", " wouldn\\'t ", " yes ", " yet ", " you ", " you\\'d ", " you\\'ll ", " you\\'re ", " you\\'ve ", " you ", " yours ", " yourself ", " yourselves ", " zero ", ]

TEXT = """
Compatibility of systems of linear constraints over the set of natural numbers
Criteria of compatibility of a system of linear Diophantine equations, strict inequations,
and nonstrict inequations are considered. Upper bounds for components of a minimal set
of solutions and algorithms of construction of minimal generating sets of solutions for all
types of systems are given. These criteria and the corresponding algorithms for
constructing a minimal supporting set of solutions can be used in solving all the
considered types of systems and systems of mixed types.
""".strip()

word_regex_map = {
    word: {
        'prefix': re.compile('^' + word + ' '),
        'suffix': re.compile(' ' + word + '$')
    } for word in COMMON_STOP_WORDS
}

punctuation_regex_map = {
    punctuation: re.compile(punctuation.strip()) for punctuation in PUTCTUATION
}


def get_candidates(text):
    separator_regex = '|'.join(PUTCTUATION + PADDED_COMMON_STOP_WORDS)

    # zero tier candidates get just separated by punctuation and common stop words
    candidates = re.split(separator_regex, text)
    candidates = [candidate.lower() for candidate in candidates]

    # first tier candidates have stuck common stop words removed from them
    stripped_candidates = []
    for candidate in candidates:
        new_candidate = candidate
        while True:
            for word in COMMON_STOP_WORDS:
                new_candidate = re.sub(word_regex_map[word]['prefix'], '', new_candidate, re.IGNORECASE)
                new_candidate = re.sub(word_regex_map[word]['suffix'], '', new_candidate, re.IGNORECASE)
            if new_candidate == candidate:
                break
            candidate = new_candidate
        stripped_candidates.append(new_candidate)

    # second tier candidates should not include common stop words
    filtered_candidates = [
        candidate for candidate in stripped_candidates if candidate not in COMMON_STOP_WORDS
    ]

    # third tier candidates get cleaned up from punctuation
    cleaned_candidates = []
    for candidate in filtered_candidates:
        for punctuation in PUTCTUATION:
            candidate = re.sub(punctuation_regex_map[punctuation], '', candidate)
        cleaned_candidates.append(candidate)

    return cleaned_candidates


def get_keyword_matrix(candidates):
    keyword_matrix = defaultdict(list)
    for candidate in candidates:
        words = candidate.split(' ')
        for word in words:
            keyword_matrix[word] += words

    deg_freq_by_keyword = {
        keyword: {
            'freq': len(vertices),
            'deg': vertices.count(keyword)
        } for keyword, vertices in keyword_matrix.items()
    }

    return deg_freq_by_keyword


def get_keywords_with_rank(candidates, keyword_matrix):
    candidate_matrix = {candidate: {'deg': 0, 'freq': 0} for candidate in candidates}
    for keyword, value in keyword_matrix.items():
        for candidate in candidate_matrix.keys():
            if keyword in candidate:
                candidate_matrix[candidate]['deg'] += value['deg']
                candidate_matrix[candidate]['freq'] += value['freq']

    return {
        key: value['freq'] / float(value['deg']) for key, value in candidate_matrix.items()
    }


def run():
    candidates = get_candidates(TEXT)
    keyword_matrix = get_keyword_matrix(candidates)
    keywords_with_rank = get_keywords_with_rank(candidates, keyword_matrix)
    print sorted(keywords_with_rank.items(), key=lambda (k, v): (v, k), reverse=True)[:len(candidates)//3]
