# ============================================================================
# ENHANCED HUMANIZER WORD LISTS - PROFESSIONAL EXPANSION
# ============================================================================

# Words that must NEVER be changed (critical for meaning preservation)
PRESERVE_WORDS = {
    # Negations (critical for meaning)
    'not', 'no', 'never', 'none', 'neither', 'nobody', 'nothing', 'nowhere',
    'nor', 'hardly', 'scarcely', 'barely', 'seldom', 'rarely',
    
    # Affirmatives
    'yes', 'all', 'every', 'always', 'everyone', 'everything', 'everywhere',
    
    # Modals (changing these alters certainty/obligation)
    'must', 'should', 'will', 'can', 'may', 'might', 'could', 'would', 
    'shall', 'ought', 'dare', 'need',
    
    # Quantifiers (preserve precision)
    'some', 'any', 'few', 'several', 'many', 'most', 'each', 'both',
    
    # Degree modifiers
    'very', 'too', 'quite', 'rather', 'fairly', 'extremely', 'highly',
    
    # Academic/Technical terms
    'data', 'study', 'research', 'analysis', 'results', 'findings', 'evidence',
    'hypothesis', 'theory', 'methodology', 'correlation', 'causation',
    'variable', 'control', 'experiment', 'observation', 'statistical',
    
    # Importance markers
    'essential', 'critical', 'important', 'significant', 'major', 'minor',
    'primary', 'secondary', 'crucial', 'vital', 'key',
    
    # Directional words
    'increase', 'decrease', 'rise', 'fall', 'grow', 'decline', 'improve',
    'worsen', 'expand', 'contract', 'enhance', 'reduce',
    
    # Logical connectors (preserve argument structure)
    'because', 'since', 'therefore', 'thus', 'hence', 'consequently',
    'if', 'then', 'unless', 'although', 'though', 'while', 'whereas',
}

# ============================================================================
# ULTRA-COMPREHENSIVE SYNONYM DATABASE (MASSIVELY EXPANDED)
# ============================================================================

ULTRA_SYNONYMS = {
    # VERBS - Action & State
    'important': ['crucial', 'vital', 'essential', 'significant', 'key', 'critical', 
                  'fundamental', 'pivotal', 'paramount', 'pressing', 'urgent', 'weighty',
                  'momentous', 'consequential', 'notable', 'central'],
    
    'show': ['demonstrate', 'illustrate', 'reveal', 'indicate', 'display', 'exhibit', 
             'present', 'showcase', 'manifest', 'expose', 'unveil', 'highlight',
             'reflect', 'convey', 'depict', 'portray', 'signal', 'evidence'],
    
    'use': ['utilize', 'employ', 'apply', 'implement', 'leverage', 'adopt', 'deploy',
            'harness', 'exercise', 'wield', 'operate', 'manipulate', 'exploit',
            'capitalize on', 'tap into', 'draw on', 'resort to', 'work with'],
    
    'make': ['create', 'produce', 'generate', 'develop', 'construct', 'establish',
             'form', 'craft', 'build', 'fashion', 'forge', 'fabricate', 'manufacture',
             'assemble', 'compose', 'devise', 'formulate', 'engineer'],
    
    'get': ['obtain', 'acquire', 'secure', 'gain', 'achieve', 'attain', 'procure',
            'receive', 'collect', 'gather', 'fetch', 'grab', 'capture', 'seize',
            'earn', 'win', 'derive', 'extract', 'pick up', 'come by'],
    
    'think': ['believe', 'consider', 'regard', 'view', 'perceive', 'deem', 'suppose',
              'reckon', 'figure', 'assume', 'presume', 'imagine', 'conceive',
              'reason', 'judge', 'feel', 'sense', 'gather', 'suspect', 'envision'],
    
    'help': ['assist', 'aid', 'support', 'facilitate', 'enable', 'contribute to',
             'boost', 'enhance', 'advance', 'further', 'promote', 'back', 'serve',
             'benefit', 'improve', 'strengthen', 'reinforce', 'complement'],
    
    'need': ['require', 'necessitate', 'demand', 'call for', 'warrant', 'entail',
             'involve', 'take', 'mandate', 'expect', 'depend on', 'rely on'],
    
    'find': ['discover', 'identify', 'locate', 'determine', 'uncover', 'detect',
             'pinpoint', 'spot', 'encounter', 'come across', 'stumble upon',
             'reveal', 'expose', 'unearth', 'dig up', 'track down'],
    
    'say': ['state', 'assert', 'declare', 'mention', 'note', 'indicate', 'express',
            'claim', 'suggest', 'propose', 'argue', 'contend', 'maintain', 'insist',
            'affirm', 'proclaim', 'announce', 'voice', 'articulate', 'convey'],
    
    'give': ['provide', 'offer', 'supply', 'furnish', 'deliver', 'present', 'grant',
             'bestow', 'confer', 'award', 'extend', 'hand over', 'pass on', 'yield',
             'donate', 'contribute', 'allocate', 'assign'],
    
    'know': ['understand', 'recognize', 'realize', 'comprehend', 'grasp', 'acknowledge',
             'appreciate', 'perceive', 'discern', 'see', 'gather', 'sense', 'be aware',
             'be conscious of', 'be familiar with', 'be versed in'],
    
    'see': ['observe', 'notice', 'perceive', 'witness', 'recognize', 'discern', 'spot',
            'detect', 'view', 'behold', 'glimpse', 'catch', 'make out', 'distinguish',
            'note', 'watch', 'monitor', 'survey'],
    
    'take': ['seize', 'grab', 'capture', 'acquire', 'adopt', 'assume', 'accept',
             'embrace', 'undertake', 'pursue', 'engage in', 'perform', 'conduct'],
    
    'put': ['place', 'position', 'set', 'situate', 'locate', 'install', 'lay',
            'rest', 'deposit', 'station', 'establish', 'fix', 'plant'],
    
    'come': ['arrive', 'approach', 'emerge', 'appear', 'surface', 'materialize',
             'show up', 'turn up', 'arise', 'originate', 'stem', 'derive'],
    
    'go': ['proceed', 'advance', 'progress', 'move', 'travel', 'head', 'journey',
           'venture', 'depart', 'leave', 'exit', 'withdraw'],
    
    'work': ['function', 'operate', 'perform', 'run', 'execute', 'labor', 'toil',
             'strive', 'endeavor', 'act', 'serve', 'do', 'handle', 'manage'],
    
    'try': ['attempt', 'endeavor', 'strive', 'seek', 'aim', 'undertake', 'venture',
            'experiment', 'test', 'sample', 'have a go at', 'take a shot at'],
    
    'ask': ['inquire', 'question', 'query', 'request', 'seek', 'petition', 'solicit',
            'demand', 'appeal', 'probe', 'interrogate', 'quiz', 'examine'],
    
    'tell': ['inform', 'notify', 'advise', 'relate', 'recount', 'report', 'communicate',
             'convey', 'reveal', 'disclose', 'divulge', 'impart', 'brief'],
    
    'feel': ['sense', 'perceive', 'experience', 'undergo', 'encounter', 'detect',
             'discern', 'notice', 'recognize', 'believe', 'think', 'consider'],
    
    'become': ['turn into', 'grow into', 'evolve into', 'transform into', 'develop into',
               'emerge as', 'end up', 'come to be', 'get to be'],
    
    'leave': ['depart', 'exit', 'quit', 'abandon', 'vacate', 'withdraw', 'retreat',
              'evacuate', 'desert', 'flee', 'escape', 'go away'],
    
    'call': ['name', 'label', 'term', 'designate', 'dub', 'christen', 'title',
             'describe as', 'refer to as', 'identify as'],
    
    'keep': ['maintain', 'preserve', 'retain', 'hold', 'sustain', 'continue',
             'uphold', 'save', 'store', 'reserve', 'safeguard'],
    
    'let': ['allow', 'permit', 'enable', 'authorize', 'sanction', 'approve',
            'grant', 'consent to', 'give permission'],
    
    'begin': ['start', 'commence', 'initiate', 'launch', 'embark on', 'set out',
              'kick off', 'get going', 'undertake', 'trigger', 'inaugurate'],
    
    'seem': ['appear', 'look', 'sound', 'feel', 'come across as', 'strike one as',
             'give the impression', 'suggest'],
    
    'turn': ['rotate', 'spin', 'revolve', 'pivot', 'swivel', 'twist', 'convert',
             'transform', 'change', 'shift', 'become'],
    
    'start': ['begin', 'commence', 'initiate', 'launch', 'kick off', 'set in motion',
              'trigger', 'spark', 'establish', 'open', 'inaugurate'],
    
    'run': ['operate', 'function', 'work', 'manage', 'direct', 'control', 'oversee',
            'administer', 'conduct', 'execute', 'sprint', 'dash'],
    
    'move': ['shift', 'relocate', 'transfer', 'transport', 'change', 'advance',
             'progress', 'proceed', 'stir', 'budge', 'migrate'],
    
    'live': ['exist', 'reside', 'dwell', 'inhabit', 'occupy', 'stay', 'remain',
             'survive', 'thrive', 'subsist', 'be'],
    
    'believe': ['think', 'feel', 'consider', 'hold', 'maintain', 'trust', 'accept',
                'suppose', 'assume', 'presume', 'suspect', 'reckon'],
    
    'bring': ['carry', 'transport', 'convey', 'deliver', 'fetch', 'take', 'bear',
              'transfer', 'introduce', 'cause', 'produce', 'generate'],
    
    'happen': ['occur', 'take place', 'transpire', 'arise', 'come about', 'develop',
               'unfold', 'emerge', 'materialize', 'result'],
    
    'write': ['compose', 'draft', 'pen', 'author', 'script', 'record', 'document',
              'inscribe', 'transcribe', 'formulate', 'articulate'],
    
    'sit': ['rest', 'settle', 'perch', 'be seated', 'recline', 'lounge', 'nestle'],
    
    'stand': ['rise', 'be upright', 'remain', 'endure', 'tolerate', 'withstand',
              'bear', 'last', 'persist', 'stay'],
    
    'lose': ['misplace', 'forfeit', 'surrender', 'sacrifice', 'relinquish', 'drop',
             'shed', 'waste', 'squander', 'be deprived of'],
    
    'pay': ['compensate', 'remunerate', 'reward', 'reimburse', 'settle', 'discharge',
            'give', 'spend', 'invest', 'disburse'],
    
    'meet': ['encounter', 'come across', 'run into', 'face', 'confront', 'greet',
             'assemble', 'gather', 'convene', 'congregate', 'satisfy', 'fulfill'],
    
    'include': ['contain', 'incorporate', 'encompass', 'comprise', 'involve', 'cover',
                'embrace', 'subsume', 'embody', 'consist of', 'take in'],
    
    'continue': ['proceed', 'persist', 'carry on', 'maintain', 'sustain', 'keep up',
                 'press on', 'go on', 'endure', 'last', 'remain'],
    
    'set': ['place', 'position', 'put', 'establish', 'determine', 'fix', 'arrange',
            'organize', 'adjust', 'define', 'specify'],
    
    'learn': ['discover', 'find out', 'grasp', 'master', 'absorb', 'acquire',
              'pick up', 'study', 'comprehend', 'understand'],
    
    'change': ['alter', 'modify', 'transform', 'adjust', 'shift', 'vary', 'adapt',
               'revise', 'amend', 'convert', 'switch', 'replace', 'exchange'],
    
    'lead': ['guide', 'direct', 'head', 'command', 'manage', 'supervise', 'govern',
             'steer', 'pilot', 'spearhead', 'result in', 'cause'],
    
    'understand': ['comprehend', 'grasp', 'recognize', 'appreciate', 'realize', 'see',
                   'perceive', 'discern', 'gather', 'fathom', 'make sense of'],
    
    'watch': ['observe', 'view', 'monitor', 'survey', 'examine', 'scrutinize',
              'look at', 'keep an eye on', 'oversee', 'supervise'],
    
    'follow': ['pursue', 'chase', 'track', 'trail', 'succeed', 'come after', 'result',
               'obey', 'adhere to', 'comply with', 'observe', 'understand', 'grasp'],
    
    'stop': ['cease', 'halt', 'end', 'terminate', 'discontinue', 'suspend', 'quit',
             'conclude', 'finish', 'pause', 'arrest', 'prevent', 'block'],
    
    'create': ['make', 'produce', 'generate', 'develop', 'form', 'establish', 'build',
               'construct', 'devise', 'invent', 'design', 'originate', 'fashion'],
    
    'speak': ['talk', 'converse', 'communicate', 'express', 'articulate', 'voice',
              'utter', 'state', 'say', 'declare', 'pronounce', 'verbalize'],
    
    'read': ['peruse', 'study', 'scan', 'review', 'examine', 'browse', 'skim',
             'interpret', 'decipher', 'understand', 'comprehend'],
    
    'spend': ['expend', 'use', 'consume', 'invest', 'devote', 'allocate', 'disburse',
              'pay out', 'waste', 'squander', 'pass', 'occupy'],
    
    'grow': ['expand', 'increase', 'develop', 'mature', 'evolve', 'flourish', 'thrive',
             'progress', 'advance', 'rise', 'swell', 'multiply', 'cultivate'],
    
    'open': ['unlock', 'unseal', 'uncover', 'expose', 'begin', 'start', 'launch',
             'initiate', 'inaugurate', 'establish', 'accessible'],
    
    'walk': ['stroll', 'stride', 'pace', 'step', 'march', 'trek', 'hike', 'wander',
             'amble', 'saunter', 'proceed on foot'],
    
    'win': ['triumph', 'prevail', 'succeed', 'conquer', 'defeat', 'beat', 'overcome',
            'achieve', 'attain', 'gain', 'secure', 'earn'],
    
    'reach': ['achieve', 'attain', 'arrive at', 'get to', 'access', 'contact',
              'extend to', 'stretch to', 'span', 'touch', 'communicate with'],
    
    'serve': ['assist', 'help', 'aid', 'support', 'provide', 'supply', 'cater',
              'function as', 'act as', 'work as', 'be useful'],
    
    'die': ['perish', 'expire', 'pass away', 'succumb', 'decease', 'fall', 'end',
            'cease', 'fade', 'vanish', 'disappear'],
    
    'send': ['dispatch', 'transmit', 'deliver', 'convey', 'forward', 'ship', 'mail',
             'post', 'transfer', 'communicate', 'relay'],
    
    'build': ['construct', 'erect', 'assemble', 'create', 'establish', 'develop',
              'form', 'make', 'fabricate', 'raise', 'fashion'],
    
    'stay': ['remain', 'continue', 'persist', 'endure', 'last', 'linger', 'wait',
             'reside', 'dwell', 'lodge', 'visit'],
    
    'fall': ['drop', 'descend', 'plummet', 'tumble', 'collapse', 'decline', 'decrease',
             'diminish', 'lower', 'sink', 'slip'],
    
    'cut': ['slice', 'chop', 'sever', 'trim', 'clip', 'shear', 'reduce', 'decrease',
            'diminish', 'lower', 'curtail', 'eliminate'],
    
    'decide': ['determine', 'resolve', 'choose', 'elect', 'opt', 'settle', 'conclude',
               'judge', 'rule', 'make up one\'s mind'],
    
    'pull': ['drag', 'draw', 'haul', 'tug', 'yank', 'tow', 'extract', 'remove',
             'attract', 'lure', 'entice'],
    
    'break': ['shatter', 'fracture', 'crack', 'split', 'burst', 'rupture', 'snap',
              'violate', 'breach', 'infringe', 'interrupt', 'disrupt'],
    
    'raise': ['lift', 'elevate', 'hoist', 'increase', 'boost', 'enhance', 'heighten',
              'bring up', 'rear', 'cultivate', 'introduce', 'present'],
    
    # ADJECTIVES - Descriptors
    'good': ['effective', 'beneficial', 'valuable', 'positive', 'advantageous', 'favorable',
             'sound', 'solid', 'excellent', 'superior', 'quality', 'fine', 'worthy',
             'useful', 'helpful', 'constructive', 'productive'],
    
    'bad': ['detrimental', 'harmful', 'negative', 'adverse', 'unfavorable', 'problematic',
            'poor', 'weak', 'inferior', 'substandard', 'deficient', 'inadequate',
            'damaging', 'destructive', 'undesirable'],
    
    'big': ['substantial', 'significant', 'considerable', 'extensive', 'large-scale',
            'major', 'sizeable', 'massive', 'huge', 'enormous', 'vast', 'immense',
            'grand', 'great', 'expansive', 'broad', 'wide-ranging'],
    
    'small': ['minor', 'limited', 'modest', 'minimal', 'slight', 'negligible', 'marginal',
              'subtle', 'tiny', 'little', 'compact', 'petty', 'insignificant',
              'trivial', 'minute', 'diminutive'],
    
    'new': ['novel', 'fresh', 'recent', 'modern', 'contemporary', 'current', 'latest',
            'innovative', 'original', 'cutting-edge', 'up-to-date', 'newfangled',
            'brand-new', 'untried'],
    
    'old': ['previous', 'former', 'past', 'earlier', 'prior', 'aged', 'ancient',
            'historic', 'vintage', 'traditional', 'established', 'outdated',
            'obsolete', 'archaic'],
    
    'high': ['elevated', 'tall', 'lofty', 'towering', 'soaring', 'great', 'intense',
             'extreme', 'strong', 'considerable', 'substantial', 'significant'],
    
    'low': ['reduced', 'minimal', 'decreased', 'limited', 'modest', 'slight', 'small',
            'minor', 'inferior', 'subordinate', 'depressed', 'shallow'],
    
    'long': ['extended', 'lengthy', 'prolonged', 'protracted', 'drawn-out', 'extensive',
             'sustained', 'enduring', 'lasting', 'lingering', 'persistent'],
    
    'short': ['brief', 'concise', 'compact', 'succinct', 'terse', 'abbreviated',
              'truncated', 'fleeting', 'momentary', 'temporary'],
    
    'different': ['distinct', 'diverse', 'varied', 'separate', 'unique', 'alternative',
                  'dissimilar', 'contrasting', 'divergent', 'disparate', 'other'],
    
    'same': ['identical', 'similar', 'equivalent', 'comparable', 'alike', 'equal',
             'matching', 'uniform', 'consistent', 'unchanged'],
    
    'clear': ['evident', 'obvious', 'apparent', 'plain', 'distinct', 'transparent',
              'lucid', 'explicit', 'unambiguous', 'understandable', 'straightforward'],
    
    'hard': ['difficult', 'challenging', 'tough', 'demanding', 'arduous', 'strenuous',
             'rigorous', 'complex', 'complicated', 'solid', 'firm', 'rigid'],
    
    'easy': ['simple', 'straightforward', 'uncomplicated', 'effortless', 'basic',
             'elementary', 'manageable', 'accessible', 'user-friendly'],
    
    'strong': ['powerful', 'robust', 'sturdy', 'solid', 'durable', 'resilient', 'tough',
               'forceful', 'intense', 'potent', 'vigorous', 'mighty'],
    
    'weak': ['feeble', 'frail', 'fragile', 'delicate', 'flimsy', 'inadequate',
             'ineffective', 'powerless', 'vulnerable', 'shaky'],
    
    'fast': ['quick', 'rapid', 'swift', 'speedy', 'hasty', 'prompt', 'expeditious',
             'brisk', 'fleet', 'accelerated'],
    
    'slow': ['gradual', 'leisurely', 'unhurried', 'sluggish', 'languid', 'delayed',
             'protracted', 'prolonged', 'tardy'],
    
    'early': ['initial', 'preliminary', 'first', 'beginning', 'premature', 'advance',
              'prior', 'preceding', 'precocious'],
    
    'late': ['delayed', 'tardy', 'overdue', 'belated', 'behind schedule', 'final',
             'concluding', 'recent', 'deceased'],
    
    'young': ['youthful', 'juvenile', 'adolescent', 'immature', 'new', 'fresh',
              'recent', 'inexperienced', 'budding'],
    
    'full': ['complete', 'entire', 'whole', 'total', 'comprehensive', 'thorough',
             'packed', 'crowded', 'loaded', 'saturated'],
    
    'hot': ['warm', 'heated', 'scorching', 'burning', 'fiery', 'torrid', 'sweltering',
            'popular', 'trending', 'intense', 'passionate'],
    
    'cold': ['cool', 'chilly', 'frigid', 'icy', 'freezing', 'frosty', 'wintry',
             'aloof', 'distant', 'unfriendly', 'unemotional'],
    
    'sure': ['certain', 'confident', 'positive', 'definite', 'convinced', 'assured',
             'guaranteed', 'reliable', 'dependable'],
    
    'true': ['accurate', 'correct', 'factual', 'genuine', 'authentic', 'real', 'valid',
             'legitimate', 'actual', 'verifiable'],
    
    'free': ['complimentary', 'gratis', 'costless', 'liberated', 'independent',
             'unrestricted', 'unconfined', 'available', 'vacant'],
    
    'able': ['capable', 'competent', 'qualified', 'skilled', 'proficient', 'adept',
             'talented', 'accomplished', 'experienced'],
    
    'ready': ['prepared', 'set', 'willing', 'eager', 'primed', 'equipped', 'available',
              'arranged', 'organized'],
    
    'simple': ['straightforward', 'basic', 'elementary', 'uncomplicated', 'plain',
               'clear', 'easy', 'modest', 'humble', 'unadorned'],
    
    'complex': ['complicated', 'intricate', 'elaborate', 'sophisticated', 'convoluted',
                'involved', 'multifaceted', 'compound', 'composite'],
    
    'recent': ['latest', 'new', 'current', 'contemporary', 'modern', 'fresh', 'up-to-date',
               'present-day'],
    
    'close': ['near', 'nearby', 'adjacent', 'neighboring', 'proximate', 'intimate',
              'tight', 'narrow', 'similar', 'comparable'],
    
    'far': ['distant', 'remote', 'faraway', 'removed', 'outlying', 'considerable',
            'substantial', 'significantly'],
    
    'common': ['widespread', 'prevalent', 'frequent', 'typical', 'usual', 'ordinary',
               'standard', 'conventional', 'normal', 'regular', 'everyday'],
    
    'rare': ['uncommon', 'unusual', 'scarce', 'infrequent', 'exceptional', 'unique',
             'extraordinary', 'singular', 'sparse'],
    
    'general': ['overall', 'broad', 'common', 'universal', 'widespread', 'comprehensive',
                'blanket', 'sweeping', 'generic', 'typical'],
    
    'specific': ['particular', 'precise', 'exact', 'definite', 'explicit', 'detailed',
                 'concrete', 'individual', 'distinct'],
    
    'whole': ['entire', 'complete', 'total', 'full', 'comprehensive', 'intact',
              'unbroken', 'undivided', 'all'],
    
    'main': ['primary', 'principal', 'chief', 'key', 'major', 'central', 'dominant',
             'leading', 'foremost', 'paramount', 'prime'],
    
    'direct': ['straight', 'immediate', 'unmediated', 'firsthand', 'personal', 'frank',
               'straightforward', 'candid', 'blunt'],
    
    'possible': ['feasible', 'viable', 'potential', 'achievable', 'attainable',
                 'practicable', 'workable', 'realistic', 'plausible'],
    
    'likely': ['probable', 'expected', 'anticipated', 'presumable', 'foreseeable',
               'predictable', 'apt', 'liable', 'prone'],
    
    'certain': ['sure', 'definite', 'guaranteed', 'inevitable', 'assured', 'confirmed',
                'established', 'undeniable', 'indisputable'],
    
    'necessary': ['essential', 'required', 'needed', 'vital', 'mandatory', 'compulsory',
                  'obligatory', 'requisite', 'indispensable', 'critical'],
    
    'major': ['significant', 'important', 'key', 'principal', 'primary', 'main',
              'substantial', 'considerable', 'serious', 'severe'],
    
    'similar': ['alike', 'comparable', 'analogous', 'parallel', 'corresponding',
                'equivalent', 'related', 'akin', 'resembling'],
    
    'real': ['actual', 'genuine', 'authentic', 'true', 'legitimate', 'bona fide',
             'veritable', 'concrete', 'tangible', 'physical'],
    
    'right': ['correct', 'accurate', 'proper', 'appropriate', 'suitable', 'fitting',
              'just', 'fair', 'moral', 'ethical'],
    
    'wrong': ['incorrect', 'inaccurate', 'mistaken', 'erroneous', 'false', 'improper',
              'inappropriate', 'unsuitable', 'unjust', 'immoral'],
    
    'better': ['superior', 'improved', 'enhanced', 'preferable', 'finer', 'greater',
               'more effective', 'more suitable'],
    
    'worse': ['inferior', 'poorer', 'lesser', 'deteriorated', 'declined', 'degraded',
              'more severe', 'more serious'],
    
    'best': ['finest', 'optimal', 'supreme', 'top', 'foremost', 'leading', 'premier',
             'outstanding', 'excellent', 'ideal', 'perfect'],
    
    'worst': ['poorest', 'least effective', 'most inferior', 'most severe', 'most terrible',
              'most dreadful', 'most dire'],
    
    'effective': ['efficient', 'successful', 'productive', 'useful', 'potent', 'powerful',
                  'impactful', 'efficacious', 'operative'],
    
    'significant': ['considerable', 'substantial', 'important', 'notable', 'major',
                    'meaningful', 'consequential', 'momentous', 'weighty'],
    
    'various': ['different', 'diverse', 'multiple', 'numerous', 'several', 'assorted',
                'varied', 'miscellaneous', 'sundry'],
    
    'appropriate': ['suitable', 'fitting', 'proper', 'apt', 'right', 'relevant',
                    'applicable', 'pertinent', 'befitting'],
    
    'available': ['accessible', 'obtainable', 'at hand', 'ready', 'on hand', 'free',
                  'usable', 'offered'],
    
    'social': ['communal', 'collective', 'public', 'societal', 'interpersonal',
               'community', 'group'],
    
    'economic': ['financial', 'monetary', 'fiscal', 'commercial', 'budgetary', 'pecuniary'],
    
    'political': ['governmental', 'civic', 'administrative', 'legislative', 'policy-related'],
    
    'natural': ['organic', 'innate', 'inherent', 'intrinsic', 'native', 'instinctive',
                'unaffected', 'authentic'],
    
    'physical': ['bodily', 'corporeal', 'material', 'tangible', 'concrete', 'substantial'],
    
    'mental': ['psychological', 'cognitive', 'intellectual', 'cerebral', 'emotional'],
    
    'positive': ['favorable', 'beneficial', 'constructive', 'optimistic', 'affirmative',
                 'advantageous', 'encouraging'],
    
    'negative': ['adverse', 'unfavorable', 'detrimental', 'harmful', 'pessimistic',
                 'disadvantageous', 'damaging'],
    
    'active': ['dynamic', 'energetic', 'busy', 'engaged', 'operational', 'functioning',
               'working', 'lively'],
    
    'passive': ['inactive', 'dormant', 'idle', 'inert', 'quiescent', 'submissive',
                'compliant', 'receptive'],
    
    'modern': ['contemporary', 'current', 'present-day', 'recent', 'up-to-date',
               'cutting-edge', 'advanced'],
    
    'traditional': ['conventional', 'customary', 'established', 'classical', 'orthodox',
                    'time-honored', 'long-standing'],
    
    'official': ['formal', 'authorized', 'legitimate', 'sanctioned', 'approved',
                 'certified', 'validated'],
    
    'private': ['personal', 'individual', 'confidential', 'secret', 'intimate',
                'exclusive', 'non-public'],
    
    'public': ['communal', 'common', 'shared', 'collective', 'open', 'accessible',
               'general', 'widespread'],
}

# ============================================================================
# DIVERSE SENTENCE STARTERS (MASSIVELY EXPANDED)
# ============================================================================

DIVERSE_STARTERS = {
    'evidence': [
        "Research reveals", "Studies show", "Evidence points to", "Analysis indicates",
        "Data suggests", "Findings demonstrate", "Investigation shows", "Examination reveals",
        "Results indicate", "Observations suggest", "Research confirms", "Evidence supports",
        "Studies demonstrate", "Data reveals", "Analysis shows", "Experiments indicate",
        "Surveys suggest", "Reports show", "Statistics reveal", "Investigations confirm",
        "Experts have found", "Scholars note", "Researchers observe", "Scientists report",
        "The data indicates", "The evidence shows", "The research suggests",
        "The findings point to", "The results demonstrate", "The analysis reveals",
        "Recent studies show", "Emerging research suggests", "Growing evidence indicates",
        "Mounting data reveals", "Accumulating studies demonstrate"
    ],
    
    'causation': [
        "This happens due to", "The reason lies in", "This stems from", "Given the fact that",
        "Considering how", "This occurs as", "The cause involves", "This arises from",
        "This results from", "The trigger is", "What drives this is", "Behind this lies",
        "The root cause is", "This can be traced to", "The source of this is",
        "What explains this is", "The underlying factor is", "At the heart of this is",
        "The key factor is", "The main driver is", "This originates from",
        "The primary reason is", "What accounts for this is", "The basis for this is",
        "The foundation of this is", "The catalyst is", "What prompts this is",
        "Given that", "Since", "As a consequence of", "Owing to the fact that"
    ],
    
    'contrast': [
        "On the flip side,", "That being said,", "In contrast,", "Conversely,",
        "On the other hand,", "Despite this,", "Yet,", "Regardless,", "Still,",
        "Even so,", "Nevertheless,", "Nonetheless,", "Having said that,",
        "At the same time,", "Alternatively,", "By contrast,", "In opposition,",
        "On the contrary,", "Unlike this,", "Whereas,", "While this is true,",
        "Then again,", "In spite of this,", "Although,", "Though this is so,",
        "Notwithstanding,", "All the same,", "Be that as it may,",
        "That said,", "In a different vein,", "From another angle,",
        "Looking at it differently,", "From another perspective,"
    ],
    
    'conclusion': [
        "This results in", "This leads to", "Consequently,", "As such,", "In turn,",
        "This means", "Ultimately,", "The outcome is", "Therefore,", "Thus,",
        "Hence,", "As a result,", "The upshot is", "The effect is",
        "What follows is", "This translates to", "The implication is",
        "The consequence is", "This brings about", "This gives rise to",
        "This culminates in", "The end result is", "This produces",
        "This generates", "This creates", "This yields", "This spawns",
        "In the end,", "Eventually,", "Finally,", "In conclusion,",
        "To sum up,", "All told,", "When all is said and done,"
    ],
    
    'addition': [
        "What's more,", "On top of that,", "Beyond that,", "In addition,",
        "Plus,", "Along with this,", "Equally important,", "Similarly,",
        "Likewise,", "By the same token,", "Not to mention,", "Another point is",
        "There's also", "We should also consider", "It's worth noting",
        "Don't forget", "We can't overlook", "Another aspect is",
        "A related point is", "Tied to this is", "Connected to this,",
        "In the same vein,", "Parallel to this,", "Complementing this,",
        "Building on this,", "Extending this further,", "Taking this further,"
    ],
    
    'emphasis': [
        "What's crucial here is", "The key point is", "Most importantly,",
        "Above all,", "Particularly noteworthy is", "Worth highlighting is",
        "It bears repeating that", "Let's be clear:", "Make no mistake:",
        "The fact remains that", "What really matters is", "At its core,",
        "Fundamentally,", "The crux of the matter is", "What stands out is",
        "Notably,", "Significantly,", "Remarkably,", "Strikingly,",
        "Of particular interest is", "What deserves attention is",
        "We must emphasize that", "It cannot be overstated that",
        "The bottom line is", "When it comes down to it,"
    ],
    
    'example': [
        "For instance,", "Take the case of", "Consider", "Look at",
        "As an illustration,", "To demonstrate,", "A case in point is",
        "One example is", "As evidence,", "To illustrate this,",
        "This is exemplified by", "We can see this in", "This shows up in",
        "A good example is", "This manifests in", "This plays out in",
        "In practice,", "In real terms,", "Practically speaking,",
        "Specifically,", "Namely,", "Such as", "Including",
        "For example,", "Like", "Say", "Picture this:"
    ],
    
    'clarification': [
        "In other words,", "Put simply,", "To put it another way,",
        "What this means is", "More specifically,", "To clarify,",
        "To be more precise,", "Breaking this down,", "Essentially,",
        "In essence,", "At bottom,", "Stripped down,", "Put differently,",
        "Another way to say this is", "The point being", "What I mean is",
        "To rephrase,", "Said differently,", "To spell it out,",
        "Let me explain:", "Here's what that means:", "In plain English,",
        "To make this clearer,", "Simply put,", "Basically,"
    ],
    
    'temporal': [
        "Initially,", "At first,", "To begin with,", "From the start,",
        "Early on,", "In the beginning,", "At the outset,",
        "Subsequently,", "Later,", "Afterward,", "Following this,",
        "Next,", "Then,", "After that,", "In time,", "Eventually,",
        "Ultimately,", "In the end,", "Finally,", "At last,",
        "Previously,", "Before this,", "Earlier,", "Prior to this,",
        "Meanwhile,", "In the meantime,", "At the same time,",
        "Simultaneously,", "Concurrently,", "At this point,", "Now,",
        "Currently,", "At present,", "These days,", "Nowadays,"
    ],
    
    'general': [
        "What matters is", "Consider how", "Essentially,", "In essence,",
        "The thing is,", "Basically,", "What's key is", "The point is",
        "Here's the deal:", "Look,", "Listen,", "The reality is",
        "Truth be told,", "To be honest,", "Frankly,", "Let's face it:",
        "At the end of the day,", "The fact is", "What we're seeing is",
        "What's happening is", "The situation is", "What's interesting is",
        "The question is", "What's worth noting is", "Keep in mind that",
        "Remember that", "Don't forget that", "It's important to realize",
        "We need to recognize", "We should understand", "It's clear that"
    ],
    
    'questioning': [
        "But what about", "What if", "Consider whether", "Could it be that",
        "Is it possible that", "Might it be", "What happens when",
        "How does this relate to", "Why is this", "What causes",
        "What explains", "How can we account for", "What's behind",
        "Where does this leave", "What are we to make of", "How should we interpret",
        "What does this tell us about", "What implications does this have for",
        "How does this affect", "What role does this play in"
    ],
    
    'agreement': [
        "This aligns with", "This supports", "This confirms", "This validates",
        "This backs up", "This corroborates", "This is consistent with",
        "This parallels", "This mirrors", "This echoes", "This reinforces",
        "In agreement with this,", "Along these lines,", "Supporting this view,",
        "Consistent with this,"
    ],
    
    'disagreement': [
        "This contradicts", "This challenges", "This disputes", "This conflicts with",
        "This goes against", "Contrary to this,", "This stands in opposition to",
        "This calls into question", "This undermines", "This counters",
        "At odds with this is", "Challenging this view,", "In contrast to this,"
    ]
}

# ============================================================================
# AI RED FLAGS - PHRASES THAT SCREAM "AI WROTE THIS"
# ============================================================================

AI_RED_FLAGS = {
    # Overly formal transitions
    r'\bit is important to note that\b': ['notably,', 'importantly,', 'bear in mind that', 'keep in mind that', 'remember that', 'note that'],
    r'\bit should be noted that\b': ['note that', 'worth noting is', 'importantly,', 'bear in mind that', 'keep in mind'],
    r'\bit is worth noting that\b': ['interestingly,', 'notably,', 'note that', 'worth mentioning is'],
    r'\bit is essential to\b': ['we must', 'it\'s vital to', 'one needs to', 'it\'s critical to', 'you need to'],
    r'\bit is crucial to\b': ['it\'s vital to', 'we must', 'one needs to', 'it\'s key to', 'you should'],
    r'\bit is imperative to\b': ['we must', 'it\'s essential to', 'one needs to', 'you need to'],
    r'\bit is critical to\b': ['it\'s vital to', 'we must', 'it\'s essential to', 'you need to'],
    
    # Conclusion markers
    r'\bin conclusion\b': ['to sum up', 'overall', 'in summary', 'ultimately', 'in the end', 'all told', 'to wrap up'],
    r'\bin summary\b': ['overall', 'to recap', 'in brief', 'essentially', 'in short', 'to sum up'],
    r'\bto summarize\b': ['in brief', 'to recap', 'in short', 'overall', 'essentially'],
    r'\ball in all\b': ['overall', 'on the whole', 'generally', 'all things considered'],
    r'\bto sum up\b': ['overall', 'in brief', 'in essence', 'basically'],
    r'\bin a nutshell\b': ['essentially', 'basically', 'simply put', 'in brief'],
    
    # Overly academic transitions
    r'\bfurthermore\b': ['what\'s more', 'on top of that', 'additionally', 'beyond that', 'plus', 'also'],
    r'\bmoreover\b': ['in addition', 'plus', 'also', 'what\'s more', 'on top of that', 'beyond that'],
    r'\badditionally\b': ['also', 'plus', 'on top of that', 'beyond that', 'what\'s more', 'too'],
    r'\bnevertheless\b': ['even so', 'still', 'yet', 'however', 'that said', 'regardless'],
    r'\bnonetheless\b': ['even so', 'still', 'yet', 'however', 'all the same'],
    r'\bconsequently\b': ['as a result', 'so', 'therefore', 'this means', 'thus', 'hence'],
    r'\bsubsequently\b': ['later', 'afterward', 'then', 'next', 'after that', 'following this'],
    r'\bthus\b': ['so', 'therefore', 'as a result', 'hence', 'this means', 'consequently'],
    r'\bhence\b': ['so', 'therefore', 'thus', 'as a result', 'for this reason'],
    r'\bthereby\b': ['in doing so', 'by this', 'through this', 'this way'],
    r'\bwherein\b': ['where', 'in which', 'and there'],
    r'\bwhereby\b': ['by which', 'through which', 'where'],
    
    # Formal intensifiers
    r'\bsignificantly\b': ['notably', 'considerably', 'substantially', 'markedly', 'greatly'],
    r'\bconsiderably\b': ['substantially', 'significantly', 'notably', 'greatly', 'markedly'],
    r'\bsubstantially\b': ['considerably', 'significantly', 'greatly', 'markedly'],
    r'\bprofoundly\b': ['deeply', 'greatly', 'seriously', 'significantly'],
    r'\bincreasingly\b': ['more and more', 'progressively', 'ever more', 'growing'],
    
    # Cliché AI phrases
    r'\bdelve into\b': ['explore', 'examine', 'look at', 'investigate', 'dig into', 'dive into'],
    r'\bdelve deeper into\b': ['explore further', 'look closer at', 'examine more thoroughly', 'dig deeper into'],
    r'\bin today\'s world\b': ['nowadays', 'currently', 'these days', 'at present', 'today'],
    r'\bin the modern world\b': ['nowadays', 'today', 'currently', 'these days'],
    r'\bin this day and age\b': ['nowadays', 'today', 'currently', 'these days'],
    r'\bat the end of the day\b': ['ultimately', 'finally', 'in the end', 'eventually', 'when all is said and done'],
    r'\bwhen all is said and done\b': ['ultimately', 'in the end', 'eventually', 'finally'],
    r'\bit goes without saying\b': ['clearly', 'obviously', 'of course', 'naturally'],
    r'\bit stands to reason\b': ['logically', 'naturally', 'it makes sense that', 'clearly'],
    r'\bby the same token\b': ['similarly', 'likewise', 'in the same way', 'along those lines'],
    
    # Hedging phrases
    r'\bto a certain extent\b': ['somewhat', 'partly', 'to some degree', 'in part'],
    r'\bto some extent\b': ['somewhat', 'partly', 'to a degree', 'in part'],
    r'\bin some ways\b': ['partly', 'to an extent', 'in certain respects'],
    r'\bto a large extent\b': ['largely', 'mostly', 'for the most part', 'generally'],
    r'\bfor the most part\b': ['mostly', 'generally', 'largely', 'usually'],
    
    # Announcement phrases
    r'\bthis article will\b': ['here we\'ll', 'we\'ll', 'this covers', 'this explores'],
    r'\bthis essay will\b': ['here we\'ll', 'this explores', 'we\'ll examine', 'this discusses'],
    r'\bthis paper will\b': ['here we\'ll', 'this examines', 'we\'ll explore', 'this discusses'],
    r'\bwe will explore\b': ['we\'ll look at', 'we\'ll examine', 'let\'s explore', 'we\'ll investigate'],
    r'\bwe will examine\b': ['we\'ll look at', 'we\'ll explore', 'let\'s examine', 'we\'ll investigate'],
    r'\bthis highlights\b': ['this shows', 'this reveals', 'this points to', 'this demonstrates'],
    r'\bthis underscores\b': ['this emphasizes', 'this highlights', 'this shows', 'this stresses'],
    
    # Generic emphasis
    r'\bof utmost importance\b': ['critical', 'crucial', 'vital', 'essential', 'key'],
    r'\bof paramount importance\b': ['critical', 'crucial', 'most important', 'vital'],
    r'\bcannot be overstated\b': ['is crucial', 'is vital', 'is critical', 'is essential'],
    r'\bplays a crucial role\b': ['is crucial for', 'is vital to', 'matters greatly for'],
    r'\bserves as a testament to\b': ['shows', 'demonstrates', 'proves', 'illustrates'],
    
    # Awkward passive constructions
    r'\bit can be seen that\b': ['we can see', 'this shows', 'clearly', 'evidently'],
    r'\bit is clear that\b': ['clearly', 'obviously', 'evidently', 'we can see'],
    r'\bit is evident that\b': ['clearly', 'obviously', 'evidently', 'it\'s clear'],
    r'\bit has been shown that\b': ['research shows', 'studies show', 'evidence shows'],
    r'\bit has been found that\b': ['researchers found', 'studies found', 'evidence shows'],
    r'\bit must be noted\b': ['note that', 'importantly', 'bear in mind'],
    r'\bit should be emphasized\b': ['note that', 'importantly', 'crucially'],
    
    # Metalanguage about the text itself
    r'\bas mentioned earlier\b': ['earlier', 'as noted', 'as I said', 'previously'],
    r'\bas previously mentioned\b': ['as noted', 'earlier', 'as I said', 'previously'],
    r'\bas discussed above\b': ['as noted', 'as mentioned', 'earlier', 'previously'],
    r'\bas noted above\b': ['as mentioned', 'earlier', 'as I said', 'previously'],
    r'\bin the following sections\b': ['next', 'below', 'in what follows', 'ahead'],
    
    # Redundant formality
    r'\bduring the course of\b': ['during', 'while', 'throughout', 'over'],
    r'\bin the event that\b': ['if', 'should', 'when', 'in case'],
    r'\bin the process of\b': ['while', 'when', 'during', 'as'],
    r'\bfor the purpose of\b': ['to', 'for', 'in order to'],
    r'\bin order to\b': ['to', 'so as to', 'for'],
    r'\bdue to the fact that\b': ['because', 'since', 'as', 'given that'],
    r'\bin light of the fact that\b': ['because', 'since', 'given that', 'considering'],
    r'\bwith regard to\b': ['regarding', 'about', 'concerning', 'on'],
    r'\bwith respect to\b': ['regarding', 'about', 'concerning', 'on'],
    r'\bin regard to\b': ['regarding', 'about', 'concerning', 'on'],
    r'\bin relation to\b': ['regarding', 'about', 'concerning', 'related to'],
    
    # AI-typical sentence patterns
    r'\bthe fact that\b': ['that', 'how', '(remove entirely if possible)'],
    r'\bthe way in which\b': ['how', 'the way', 'how exactly'],
    r'\bthe extent to which\b': ['how much', 'how far', 'to what degree'],
    r'\bthe manner in which\b': ['how', 'the way', 'how exactly'],
    r'\bthe degree to which\b': ['how much', 'how far', 'to what extent'],
    
    # Overused metaphors
    r'\bshed light on\b': ['reveal', 'clarify', 'explain', 'illuminate', 'show'],
    r'\bcast light on\b': ['reveal', 'clarify', 'explain', 'show'],
    r'\bpave the way for\b': ['enable', 'allow', 'make possible', 'facilitate'],
    r'\bopen the door to\b': ['enable', 'allow', 'make possible', 'create opportunities for'],
    r'\bbring to light\b': ['reveal', 'expose', 'uncover', 'show'],
    r'\bcome to light\b': ['emerge', 'appear', 'become known', 'surface'],
    
    # Flowery language
    r'\ba myriad of\b': ['many', 'numerous', 'countless', 'various'],
    r'\ba plethora of\b': ['many', 'numerous', 'plenty of', 'lots of'],
    r'\ba multitude of\b': ['many', 'numerous', 'countless', 'various'],
    r'\ba wide array of\b': ['many', 'various', 'numerous', 'different'],
    r'\ba broad spectrum of\b': ['many', 'various', 'diverse', 'different'],
    r'\ba diverse range of\b': ['many', 'various', 'different', 'diverse'],
    
    # Buzzword combinations
    r'\brobust and comprehensive\b': ['thorough', 'complete', 'detailed', 'extensive'],
    r'\bcomplex and multifaceted\b': ['complicated', 'intricate', 'complex', 'layered'],
    r'\bvast and varied\b': ['extensive', 'wide-ranging', 'diverse', 'broad'],
    r'\brich and diverse\b': ['varied', 'diverse', 'extensive', 'wide-ranging'],
}

# ============================================================================
# ADDITIONAL CRITICAL LISTS FOR HUMANIZATION
# ============================================================================

# Contractions to make text more conversational
CONTRACTIONS_MAP = {
    'do not': 'don\'t',
    'does not': 'doesn\'t',
    'did not': 'didn\'t',
    'will not': 'won\'t',
    'would not': 'wouldn\'t',
    'should not': 'shouldn\'t',
    'could not': 'couldn\'t',
    'cannot': 'can\'t',
    'is not': 'isn\'t',
    'are not': 'aren\'t',
    'was not': 'wasn\'t',
    'were not': 'weren\'t',
    'have not': 'haven\'t',
    'has not': 'hasn\'t',
    'had not': 'hadn\'t',
    'will have': 'will\'ve',
    'would have': 'would\'ve',
    'could have': 'could\'ve',
    'should have': 'should\'ve',
    'might have': 'might\'ve',
    'must have': 'must\'ve',
    'I am': 'I\'m',
    'you are': 'you\'re',
    'he is': 'he\'s',
    'she is': 'she\'s',
    'it is': 'it\'s',
    'we are': 'we\'re',
    'they are': 'they\'re',
    'I have': 'I\'ve',
    'you have': 'you\'ve',
    'we have': 'we\'ve',
    'they have': 'they\'ve',
    'I would': 'I\'d',
    'you would': 'you\'d',
    'he would': 'he\'d',
    'she would': 'she\'d',
    'we would': 'we\'d',
    'they would': 'they\'d',
    'I will': 'I\'ll',
    'you will': 'you\'ll',
    'he will': 'he\'ll',
    'she will': 'she\'ll',
    'we will': 'we\'ll',
    'they will': 'they\'ll',
    'that is': 'that\'s',
    'there is': 'there\'s',
    'here is': 'here\'s',
    'what is': 'what\'s',
    'who is': 'who\'s',
    'where is': 'where\'s',
    'when is': 'when\'s',
    'why is': 'why\'s',
    'how is': 'how\'s',
}

# Filler words/phrases humans use (use sparingly!)
HUMAN_FILLERS = [
    'you know', 'I mean', 'kind of', 'sort of', 'basically',
    'actually', 'literally', 'honestly', 'frankly', 'clearly',
    'obviously', 'of course', 'naturally', 'essentially',
    'really', 'just', 'pretty much', 'more or less',
    'in a way', 'in a sense', 'to some degree', 'somewhat',
    'relatively', 'fairly', 'rather', 'quite', 'perhaps',
    'maybe', 'possibly', 'probably', 'likely', 'arguably',
]

# Sentence length variety markers (use to vary rhythm)
RHYTHM_MARKERS = {
    'short_starters': [
        'Look.', 'Listen.', 'True.', 'Fair enough.', 'Sure.', 'Right.',
        'Exactly.', 'Indeed.', 'Granted.', 'Still.', 'Yet.', 'Now.',
        'Then.', 'So.', 'Why?', 'How?', 'What?', 'When?', 'Where?'
    ],
    'medium_connectors': [
        'Here\'s the thing:', 'Think about it:', 'Consider this:',
        'The reality is:', 'What matters is:', 'The point is:',
        'The question becomes:', 'What\'s interesting is:',
        'What we see is:', 'What happens is:', 'The truth is:'
    ],
    'long_builders': [
        'What this really comes down to is', 'When you think about it carefully',
        'If we take a step back and look at', 'What becomes clear when we examine',
        'The interesting thing that emerges is', 'What we need to understand is'
    ]
}

# Punctuation variety (use to create flow)
PUNCTUATION_PATTERNS = {
    'emphasis': ['!', '?!', '...', '—'],
    'casual': [' - ', ', ', '; ', ': '],
    'formal': ['; ', ': ', '. ', ', '],
}

# Words that indicate AI-written passive voice patterns to avoid
PASSIVE_INDICATORS = {
    'is being', 'are being', 'was being', 'were being',
    'is shown', 'are shown', 'was shown', 'were shown',
    'is seen', 'are seen', 'was seen', 'were seen',
    'is found', 'are found', 'was found', 'were found',
    'is considered', 'are considered', 'was considered', 'were considered',
    'is believed', 'are believed', 'was believed', 'were believed',
    'is thought', 'are thought', 'was thought', 'were thought',
    'is known', 'are known', 'was known', 'were known',
    'is understood', 'are understood', 'was understood', 'were understood',
    'is recognized', 'are recognized', 'was recognized', 'were recognized',
}

# Human-like informal expressions
INFORMAL_REPLACEMENTS = {
    r'\bhowever\b': ['but', 'though', 'yet', 'still', 'that said'],
    r'\btherefore\b': ['so', 'thus', 'hence', 'which means', 'meaning'],
    r'\balthough\b': ['though', 'even though', 'while', 'despite'],
    r'\bbecause\b': ['since', 'as', 'given that', 'seeing as', 'considering'],
    r'\bamong\b': ['between', 'with', 'in'],
    r'\bregarding\b': ['about', 'on', 'concerning'],
    r'\bconcerning\b': ['about', 'on', 'regarding'],
    r'\butilize\b': ['use', 'employ', 'apply'],
    r'\bdemonstrate\b': ['show', 'prove', 'reveal'],
    r'\bfacilitate\b': ['help', 'ease', 'enable'],
    r'\bimplement\b': ['use', 'apply', 'put into action'],
}

# ============================================================================
# SENTENCE STRUCTURE PATTERNS (Critical for reducing AI detection)
# ============================================================================

# Vary sentence openings - AI tends to start with subject-verb
SENTENCE_OPENING_PATTERNS = {
    'prepositional': [
        'In {noun},', 'At {noun},', 'On {noun},', 'By {noun},', 
        'Through {noun},', 'With {noun},', 'From {noun},', 'For {noun},',
        'During {noun},', 'After {noun},', 'Before {noun},', 'Under {noun},'
    ],
    'adverbial': [
        'Interestingly,', 'Surprisingly,', 'Notably,', 'Importantly,',
        'Remarkably,', 'Curiously,', 'Oddly,', 'Strangely,', 'Clearly,',
        'Obviously,', 'Evidently,', 'Apparently,', 'Certainly,', 'Surely,'
    ],
    'transitional': [
        'Meanwhile,', 'Later,', 'Soon,', 'Then,', 'Now,', 'Next,',
        'First,', 'Second,', 'Finally,', 'Eventually,', 'Initially,',
        'Subsequently,', 'Afterward,', 'Previously,'
    ],
    'dependent_clause': [
        'When {subject} {verb},', 'While {subject} {verb},', 'If {subject} {verb},',
        'Although {subject} {verb},', 'Because {subject} {verb},', 'Since {subject} {verb},',
        'Unless {subject} {verb},', 'As {subject} {verb},', 'Though {subject} {verb},'
    ],
    'participial': [
        'Looking at {noun},', 'Considering {noun},', 'Given {noun},',
        'Examining {noun},', 'Taking {noun},', 'Using {noun},',
        'Following {noun},', 'Seeing {noun},', 'Understanding {noun},'
    ],
    'question': [
        'What about {noun}?', 'Why does {subject} {verb}?', 'How can {subject} {verb}?',
        'Where does {subject} {verb}?', 'When should {subject} {verb}?',
        'Who {verb} {noun}?', 'Which {noun} {verb}?'
    ],
    'exclamatory': [
        'What a {adjective} {noun}!', 'How {adjective}!', 'Such {noun}!',
    ],
}

# Sentence length patterns - vary to avoid AI's predictable rhythm
SENTENCE_LENGTH_TARGETS = {
    'very_short': (3, 7),      # 3-7 words - "It works. Simple as that."
    'short': (8, 12),          # 8-12 words - "This approach solves the problem effectively."
    'medium': (13, 20),        # 13-20 words - More complex ideas
    'long': (21, 30),          # 21-30 words - Complex thoughts with clauses
    'very_long': (31, 45),     # 31-45 words - Use sparingly for variety
}

# Ideal distribution for human-like writing
SENTENCE_LENGTH_DISTRIBUTION = {
    'very_short': 0.15,   # 15% of sentences
    'short': 0.30,        # 30% of sentences
    'medium': 0.35,       # 35% of sentences
    'long': 0.15,         # 15% of sentences
    'very_long': 0.05,    # 5% of sentences
}

# ============================================================================
# PARAGRAPH STRUCTURE PATTERNS
# ============================================================================

PARAGRAPH_PATTERNS = {
    'topic_sentence_styles': [
        'Direct statement', 'Question', 'Bold claim', 'Statistic',
        'Quote', 'Anecdote', 'Contrast', 'Problem statement'
    ],
    'development_strategies': [
        'Example → Explanation', 'Cause → Effect', 'Problem → Solution',
        'Claim → Evidence', 'General → Specific', 'Chronological',
        'Compare/Contrast', 'Process steps'
    ],
    'conclusion_styles': [
        'Summary', 'Implication', 'Question', 'Bridge to next',
        'Call to action', 'Broader context', 'Clincher statement'
    ]
}

# Ideal paragraph length variety (in sentences)
PARAGRAPH_LENGTH_TARGETS = {
    'very_short': (1, 2),     # For emphasis or transitions
    'short': (3, 4),          # Quick points
    'medium': (5, 7),         # Standard paragraphs
    'long': (8, 12),          # Detailed explanations
}

# ============================================================================
# VOCABULARY SOPHISTICATION LEVELS
# ============================================================================

# Mix these levels to avoid AI's tendency toward consistent formality
VOCAB_SOPHISTICATION = {
    'basic': {  # Everyday words
        'get', 'make', 'do', 'go', 'see', 'know', 'think', 'want',
        'good', 'bad', 'big', 'small', 'new', 'old', 'right', 'wrong'
    },
    'intermediate': {  # Common educated vocabulary
        'obtain', 'create', 'achieve', 'understand', 'consider', 'provide',
        'effective', 'significant', 'important', 'various', 'different'
    },
    'advanced': {  # More sophisticated but not pretentious
        'acquire', 'facilitate', 'demonstrate', 'comprehend', 'analyze',
        'substantial', 'considerable', 'diverse', 'distinct', 'notable'
    },
    'academic': {  # Use sparingly to avoid AI detection
        'procure', 'engender', 'elucidate', 'apprehend', 'scrutinize',
        'preponderant', 'multifarious', 'disparate', 'salient'
    }
}

# Ideal distribution for natural writing
VOCAB_DISTRIBUTION = {
    'basic': 0.50,          # 50% everyday words
    'intermediate': 0.30,   # 30% common educated words
    'advanced': 0.15,       # 15% sophisticated words
    'academic': 0.05,       # 5% academic words (use carefully!)
}

# ============================================================================
# TONE MARKERS
# ============================================================================

TONE_INDICATORS = {
    'casual': [
        'pretty', 'really', 'quite', 'fairly', 'rather', 'kind of',
        'sort of', 'a bit', 'somewhat', 'a little', 'pretty much',
        'basically', 'essentially', 'generally', 'typically'
    ],
    'confident': [
        'clearly', 'obviously', 'certainly', 'definitely', 'absolutely',
        'undoubtedly', 'unquestionably', 'without doubt', 'for sure',
        'no doubt', 'indeed', 'surely', 'truly'
    ],
    'hedging': [
        'perhaps', 'maybe', 'possibly', 'probably', 'likely', 'might',
        'could', 'may', 'seems', 'appears', 'suggests', 'indicates',
        'tends to', 'often', 'generally', 'usually', 'typically'
    ],
    'emphatic': [
        'very', 'extremely', 'highly', 'particularly', 'especially',
        'incredibly', 'remarkably', 'notably', 'significantly',
        'substantially', 'considerably', 'profoundly', 'deeply'
    ],
    'conversational': [
        'you know', 'I mean', 'let\'s face it', 'truth be told',
        'to be honest', 'frankly', 'honestly', 'look', 'listen',
        'here\'s the thing', 'the thing is', 'what\'s more',
        'in fact', 'actually', 'really', 'anyway'
    ]
}

# ============================================================================
# COMMON AI WRITING PATTERNS TO AVOID
# ============================================================================

AI_PATTERNS_TO_AVOID = {
    # Perfect symmetry in lists
    'symmetrical_lists': 'Avoid lists where every item has identical structure',
    
    # Overuse of semicolons
    'semicolon_abuse': 'AI loves semicolons; humans use them sparingly',
    
    # Starting every paragraph with topic sentences
    'rigid_topic_sentences': 'Vary how paragraphs begin',
    
    # Consistent sentence length
    'uniform_rhythm': 'Mix short, punchy sentences with longer, flowing ones',
    
    # Perfect grammar always
    'flawless_grammar': 'Humans occasionally break rules for effect',
    
    # No contractions
    'no_contractions': 'Use contractions to sound natural',
    
    # Three-item lists everywhere
    'rule_of_three': 'Not everything needs to come in threes',
    
    # Balanced paragraphs
    'uniform_paragraphs': 'Vary paragraph length dramatically',
    
    # No fragments
    'no_fragments': 'Strategic fragments work. They add punch.',
    
    # Perfect transitions
    'smooth_transitions': 'Humans sometimes jump between ideas',
    
    # Consistent formality
    'uniform_tone': 'Mix casual and formal elements naturally',
    
    # Overexplaining
    'excessive_clarity': 'Humans assume shared knowledge sometimes',
}

# ============================================================================
# HUMANIZATION STRATEGIES
# ============================================================================

HUMANIZATION_TECHNIQUES = {
    'vary_sentence_openings': 'Start sentences differently - not always subject-verb',
    'mix_sentence_lengths': 'Combine very short and very long sentences',
    'use_contractions': 'Don\'t avoid contractions - they\'re natural',
    'add_personality': 'Inject opinions, attitudes, or perspective',
    'strategic_fragments': 'Use incomplete sentences. For emphasis.',
    'conversational_asides': 'Add parenthetical thoughts (like this)',
    'rhetorical_questions': 'Why not engage the reader directly?',
    'informal_connectors': 'Use "but" and "so" to start sentences',
    'active_voice_priority': 'Prefer "researchers found" over "it was found"',
    'specific_over_generic': 'Replace vague terms with concrete details',
    'remove_hedging': 'Cut unnecessary qualifiers and softeners',
    'vary_paragraph_rhythm': 'Mix one-sentence paragraphs with longer ones',
    'authentic_transitions': 'Not every idea needs a formal connector',
    'embrace_informality': 'Academic doesn\'t mean robotic',
    'personal_pronouns': 'Use "we," "you," "I" when appropriate',
}

# ============================================================================
# DETECTION REDUCTION STRATEGIES
# ============================================================================

ANTI_DETECTION_RULES = {
    'rule_1': 'Remove 90% of adverbs ending in -ly',
    'rule_2': 'Replace passive voice with active voice',
    'rule_3': 'Cut all "in order to" → "to"',
    'rule_4': 'Eliminate "the fact that" constructions',
    'rule_5': 'Replace "which" with "that" in restrictive clauses',
    'rule_6': 'Use contractions in 30-50% of opportunities',
    'rule_7': 'Vary sentence length: aim for 15-word average, 10-word std dev',
    'rule_8': 'Start 20% of sentences with non-subject openings',
    'rule_9': 'Include 2-3 very short sentences (under 5 words) per 100 words',
    'rule_10': 'Use one fragment per 200-300 words for emphasis',
    'rule_11': 'Replace 50% of formal transitions with casual ones',
    'rule_12': 'Add occasional colloquialisms appropriate to context',
    'rule_13': 'Break one "grammar rule" per 150 words (strategically)',
    'rule_14': 'Vary paragraph length: 1-10 sentences',
    'rule_15': 'Use rhetorical questions sparingly (1 per 300 words)',
}

# ============================================================================
# CONTEXT-SPECIFIC REPLACEMENTS
# ============================================================================

# Academic writing (more formal but still human)
ACADEMIC_REPLACEMENTS = {
    'studies show': ['research indicates', 'evidence suggests', 'data reveals', 'analysis shows'],
    'it is important': ['significantly', 'critically', 'notably', 'vitally'],
    'there are many': ['numerous', 'various', 'multiple', 'several'],
    'in conclusion': ['ultimately', 'in sum', 'overall', 'finally'],
}

# Business writing (professional but direct)
BUSINESS_REPLACEMENTS = {
    'at this point in time': ['now', 'currently', 'at present'],
    'in the near future': ['soon', 'shortly', 'within weeks'],
    'due to the fact that': ['because', 'since', 'as'],
    'in regards to': ['regarding', 'about', 'concerning'],
}

# Creative writing (more varied and expressive)
CREATIVE_REPLACEMENTS = {
    'very': ['incredibly', 'remarkably', 'extraordinarily', 'exceptionally'],
    'said': ['whispered', 'declared', 'muttered', 'announced', 'stated'],
    'walked': ['strolled', 'strode', 'ambled', 'wandered', 'marched'],
    'looked': ['glanced', 'gazed', 'peered', 'stared', 'observed'],
}

# ============================================================================
# PUNCTUATION VARIATION PATTERNS
# ============================================================================

PUNCTUATION_STRATEGIES = {
    'em_dash_uses': [
        'Interruption: The plan—if we can call it that—failed.',
        'Emphasis: She had one goal—survival.',
        'List introduction: Three things matter—time, money, effort.',
        'Afterthought: He left—never to return.'
    ],
    'semicolon_uses': [
        'Related clauses: The rain fell; the streets flooded.',
        'Complex lists: Cities visited: Paris, France; Rome, Italy; Berlin, Germany.',
    ],
    'colon_uses': [
        'Explanation: One thing is certain: change is coming.',
        'List introduction: Consider these factors: cost, time, quality.',
        'Emphasis: The verdict: guilty.',
    ],
    'parentheses_uses': [
        'Aside: The results (as expected) were positive.',
        'Clarification: The CEO (John Smith) resigned.',
        'Citation: Research shows benefits (Johnson, 2023).',
    ],
}

# ============================================================================
# INTENSITY MODIFIERS (for varied emphasis)
# ============================================================================

INTENSITY_LEVELS = {
    'minimal': ['slightly', 'somewhat', 'a bit', 'rather', 'fairly', 'relatively'],
    'moderate': ['quite', 'pretty', 'fairly', 'reasonably', 'moderately'],
    'strong': ['very', 'really', 'highly', 'extremely', 'particularly'],
    'extreme': ['incredibly', 'exceptionally', 'extraordinarily', 'remarkably', 'profoundly'],
}

# ============================================================================
# CAUSAL CONNECTORS (variety for cause-effect relationships)
# ============================================================================

CAUSAL_CONNECTORS = {
    'direct_cause': ['because', 'since', 'as', 'due to', 'owing to', 'given that'],
    'result': ['so', 'therefore', 'thus', 'hence', 'consequently', 'as a result'],
    'purpose': ['to', 'in order to', 'so that', 'for the purpose of'],
    'condition': ['if', 'unless', 'provided that', 'on condition that', 'assuming'],
}

# ============================================================================
# EVIDENCE INTRODUCERS (for supporting claims)
# ============================================================================

EVIDENCE_PHRASES = {
    'research': [
        'Research shows', 'Studies indicate', 'Evidence suggests', 
        'Data reveals', 'Findings demonstrate', 'Analysis shows',
        'Investigations reveal', 'Experiments prove', 'Surveys find'
    ],
    'expert': [
        'Experts argue', 'Scholars suggest', 'Researchers claim',
        'Scientists report', 'Analysts note', 'Specialists observe'
    ],
    'example': [
        'For instance', 'For example', 'Take the case of', 'Consider',
        'As seen in', 'Illustrated by', 'Demonstrated by', 'Such as'
    ],
    'statistic': [
        'Statistics show', 'Data indicates', 'Numbers reveal',
        'Figures demonstrate', 'Records show', 'Metrics indicate'
    ],
}

# ============================================================================
# CONCLUSION SIGNALS (varied ways to wrap up)
# ============================================================================

CONCLUSION_SIGNALS = {
    'summary': ['In sum', 'Overall', 'In brief', 'To recap', 'In short'],
    'final': ['Ultimately', 'Finally', 'In the end', 'Eventually', 'At last'],
    'implication': ['This means', 'This suggests', 'This implies', 'The upshot is'],
    'emphasis': ['The point is', 'What matters is', 'The key is', 'Essentially'],
}

# ============================================================================
# USAGE INSTRUCTIONS AND NOTES
# ============================================================================

HUMANIZER_NOTES = """
KEY PRINCIPLES FOR REDUCING AI DETECTION:

1. SENTENCE VARIETY IS CRUCIAL
   - Mix lengths: very short (3-7 words), short (8-12), medium (13-20), long (21-30)
   - Vary openings: don't always start with subject-verb
   - Use fragments strategically for emphasis
   - Break up monotonous rhythm

2. VOCABULARY MIXING
   - Blend basic, intermediate, and advanced words
   - Avoid consistent formality level
   - Use contractions naturally (30-50% of opportunities)
   - Replace AI-flagged words from AI_RED_FLAGS dictionary

3. STRUCTURAL VARIATION
   - Vary paragraph lengths dramatically (1-10 sentences)
   - Don't make every paragraph follow topic-sentence pattern
   - Use short paragraphs for emphasis
   - Occasionally start with questions or bold claims

4. TONE AUTHENTICITY
   - Add conversational elements where appropriate
   - Include hedging or confidence markers naturally
   - Use informal connectors ("but", "so") to start sentences
   - Add personality through word choice

5. PUNCTUATION DIVERSITY
   - Use em dashes for interruption or emphasis
   - Don't overuse semicolons (AI tendency)
   - Employ parenthetical asides
   - Vary punctuation for rhythm

6. ANTI-AI PATTERNS
   - Remove passive voice constructions
   - Cut unnecessary adverbs (-ly words)
   - Eliminate redundant phrases
   - Replace formal transitions with casual ones
   - Avoid perfect symmetry in structure

7. CONTEXT MATTERS
   - Academic: more formal but still varied
   - Business: professional but direct
   - Creative: highly varied and expressive
   - Casual: conversational and natural

CRITICAL: The goal is not to make text "simpler" but to make it more 
HUMAN - which means more varied, less predictable, and naturally imperfect.

AI writes in patterns. Humans write with personality.
"""

# ============================================================================
# SCORING WEIGHTS FOR HUMANIZATION
# ============================================================================

HUMANIZATION_WEIGHTS = {
    'sentence_length_variety': 0.20,      # 20% - Critical for detection
    'vocabulary_diversity': 0.15,         # 15% - Important but not primary
    'transition_naturalness': 0.15,       # 15% - AI flags formal transitions
    'contraction_usage': 0.10,            # 10% - Simple but effective
    'paragraph_variety': 0.10,            # 10% - Structural diversity
    'opening_variety': 0.10,              # 10% - Sentence start patterns
    'active_voice_ratio': 0.08,           # 8% - Avoid passive constructions
    'punctuation_diversity': 0.07,        # 7% - Rhythm and flow
    'tone_consistency': 0.05,             # 5% - Appropriate to context
}

# End of enhanced word lists