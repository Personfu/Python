# Communication Theory — Comprehensive Guide

## COM 263 | Portland Community College | Spring 2026

| Field             | Value                                    |
|-------------------|------------------------------------------|
| **Author**        | Preston Furulie                          |
| **Organization**  | FLLC Enterprise                          |
| **Department**    | Professional Development                 |
| **Course**        | COM 263 — Interpersonal Communication    |

---

## 1. Communication Models

### 1.1 Linear Model (Shannon-Weaver, 1949)

The linear model treats communication as a **one-way process** from sender to
receiver. Originally developed for telephone engineering, it remains useful for
understanding broadcast communication.

```
Sender → Encoder → Channel → Decoder → Receiver
                      ↑
                    Noise
```

| Component    | Definition                                           | Example                        |
|--------------|------------------------------------------------------|--------------------------------|
| Sender       | Originator of the message                            | IT manager writing an email    |
| Encoder      | Translates thoughts into transmittable form          | Typing words, choosing tone    |
| Channel      | Medium through which message travels                 | Email, phone, Slack, in-person |
| Decoder      | Translates received signal back into meaning         | Reading the email              |
| Receiver     | Intended audience of the message                     | Team member                    |
| Noise        | Anything that distorts or interferes with the message| Jargon, poor signal, distraction|

**Limitations:** No feedback mechanism; assumes passive receiver; oversimplifies
real communication.

### 1.2 Interactive Model (Schramm, 1954)

The interactive model adds **feedback** and recognizes that both parties encode
and decode messages, but treats communication as alternating turns.

```
       ┌──── Message ────→
Sender ←                    Receiver
       └──── Feedback ────┘
       
  [Field of            [Field of
   Experience]          Experience]
```

| Enhancement          | Description                                        |
|----------------------|----------------------------------------------------|
| Feedback             | Receiver's response back to the sender             |
| Field of Experience  | Each person's background, culture, knowledge       |
| Shared Experience    | Overlap where mutual understanding occurs          |

**Key Insight:** Communication is most effective when the fields of experience
overlap significantly. In IT teams, shared technical vocabulary creates this overlap.

### 1.3 Transactional Model (Barnlund, 1970)

The transactional model treats communication as a **simultaneous, continuous
process** where both parties are simultaneously senders and receivers.

| Characteristic       | Description                                        |
|-----------------------|----------------------------------------------------|
| Simultaneous          | Both parties send and receive at the same time     |
| Context-dependent     | Physical, social, cultural, temporal contexts matter|
| Relational            | Communication shapes and is shaped by relationships|
| Irreversible          | Messages cannot be "taken back"                    |
| Dynamic               | Meaning is co-created in real time                 |

**Application in IT:** During a technical meeting, while one person speaks
(verbal message), others are simultaneously sending nonverbal feedback (nodding,
confusion, note-taking) that the speaker processes in real time.

### 1.4 Model Comparison

| Feature              | Linear           | Interactive        | Transactional       |
|----------------------|------------------|--------------------|---------------------|
| Direction            | One-way          | Two-way (turns)    | Simultaneous        |
| Feedback             | None             | Delayed            | Continuous          |
| Roles                | Fixed            | Alternating        | Simultaneous        |
| Context              | Ignored          | Partial            | Central             |
| Best Represents      | Broadcasts, memos| Email exchanges    | Face-to-face, video |

---

## 2. Communication Components in Depth

### 2.1 The Seven Components

| Component   | Definition                                         | IT Workplace Example                  |
|-------------|----------------------------------------------------|---------------------------------------|
| Sender      | Person initiating the communication                | Developer submitting a pull request   |
| Receiver    | Person interpreting the message                    | Code reviewer reading the PR          |
| Message     | Content being communicated                         | Code changes and PR description       |
| Channel     | Medium of transmission                             | GitHub, Slack, email, standup meeting |
| Noise       | Interference with accurate reception               | Technical jargon to non-tech audience |
| Feedback    | Receiver's response indicating understanding       | Review comments, approval, questions  |
| Context     | Environment and circumstances of communication     | Sprint deadline, team dynamics        |

### 2.2 Types of Noise

| Noise Type      | Definition                                    | Example                              |
|-----------------|-----------------------------------------------|--------------------------------------|
| Physical        | Environmental interference                    | Loud data center during walkthrough  |
| Physiological   | Biological factors affecting reception        | Fatigue during a late-night on-call  |
| Psychological   | Mental/emotional interference                 | Stress about an upcoming deadline    |
| Semantic        | Misinterpretation of word meaning             | "Server" meaning hardware vs software|
| Cultural        | Differences in cultural interpretation        | Direct vs indirect communication     |
| Technical       | Technology-related interference               | Bad audio on a video call            |

---

## 3. Verbal vs Nonverbal Communication

### 3.1 Verbal Communication

| Aspect           | Description                                        |
|------------------|----------------------------------------------------|
| Denotation       | Dictionary definition of words                     |
| Connotation      | Emotional/cultural associations of words            |
| Jargon           | Specialized vocabulary for a field                  |
| Abstraction      | Level of specificity (abstract ↔ concrete)         |
| Tone             | Vocal quality conveying attitude                    |
| Register         | Formality level (casual ↔ formal)                  |

### 3.2 Nonverbal Communication

Research suggests **55-93%** of emotional meaning comes from nonverbal cues.

| Category        | Elements                                           | Workplace Impact                     |
|-----------------|----------------------------------------------------|--------------------------------------|
| Kinesics        | Facial expressions, gestures, posture              | Confidence in presentations          |
| Proxemics       | Use of personal space                              | Meeting seating arrangements         |
| Haptics         | Touch-based communication                          | Handshakes in professional settings  |
| Chronemics      | Use of time                                        | Punctuality signals respect          |
| Paralanguage    | Vocal tone, pitch, speed, volume                   | Enthusiasm in team meetings          |
| Artifacts       | Clothing, objects, environment                     | Professional appearance at clients   |
| Oculesics       | Eye contact patterns                               | Engagement during presentations      |

### 3.3 Nonverbal in Virtual Communication

| Challenge                    | Mitigation Strategy                              |
|------------------------------|--------------------------------------------------|
| Limited body language        | Use camera on; exaggerate facial expressions     |
| No eye contact cues          | Look at camera when speaking                     |
| Missed social cues           | Use reactions/emojis in chat                     |
| Turn-taking confusion        | Use hand-raise features; establish protocols     |
| Background distractions      | Use virtual backgrounds; mute when not speaking  |

---

## 4. Listening Styles

### 4.1 Types of Listening

| Style          | Focus                         | When to Use                          | IT Example                          |
|----------------|-------------------------------|--------------------------------------|-------------------------------------|
| Active         | Full engagement and response  | Team meetings, 1-on-1s              | Sprint retrospective discussions    |
| Empathetic     | Understanding emotions        | Conflict resolution, support        | Helping frustrated end users        |
| Critical       | Evaluating logic and evidence | Decision-making, reviews            | Evaluating vendor proposals         |
| Appreciative   | Enjoyment and inspiration     | Conferences, team celebrations      | Keynote at a tech conference        |
| Informational  | Learning and understanding    | Training, onboarding                | New employee learning systems       |

### 4.2 Active Listening Techniques

| Technique         | Description                                       | Example                             |
|-------------------|---------------------------------------------------|-------------------------------------|
| Paraphrasing      | Restating in your own words                       | "So the server is dropping packets?"|
| Reflecting        | Mirroring the speaker's emotions                  | "That sounds frustrating."          |
| Clarifying        | Asking for more detail                            | "Can you walk me through the error?"|
| Summarizing       | Condensing key points                             | "To recap, the three priorities..." |
| Minimal encouragers| Brief verbal/nonverbal cues                      | "I see," nodding, "Go on"          |
| Open questions    | Questions requiring more than yes/no              | "What have you tried so far?"       |

### 4.3 Barriers to Effective Listening

| Barrier              | Description                                      |
|----------------------|--------------------------------------------------|
| Pseudolistening      | Appearing to listen without processing            |
| Selective listening   | Only hearing what you want to hear               |
| Defensive listening   | Taking neutral comments as personal attacks      |
| Ambushing            | Listening only to find points to attack          |
| Multitasking         | Dividing attention (checking phone in meetings)  |
| Premature judgment   | Forming conclusions before the speaker finishes  |

---

## 5. Perception

### 5.1 The Perception Process

| Stage              | Description                                       | Example                             |
|--------------------|---------------------------------------------------|-------------------------------------|
| **Selection**      | Choosing which stimuli to attend to               | Noticing a coworker's tone change   |
| **Organization**   | Structuring selected info into patterns           | Categorizing behavior as "upset"    |
| **Interpretation** | Assigning meaning to organized information        | Deciding they're upset about the bug|
| **Negotiation**    | Sharing perceptions to reach shared meaning       | Asking "Is everything okay?"        |

### 5.2 Perception Influences

| Factor              | Description                                       |
|---------------------|---------------------------------------------------|
| Physiological       | Physical state affects what we notice and how     |
| Cultural            | Cultural background shapes interpretation         |
| Social roles        | Job title and status influence perception          |
| Self-concept        | How we see ourselves colors how we see others     |
| Cognitive biases    | Halo effect, confirmation bias, attribution error |

### 5.3 Common Perception Errors

| Error                         | Description                                  |
|-------------------------------|----------------------------------------------|
| Fundamental Attribution Error | Attributing others' behavior to character     |
| Self-Serving Bias             | Attributing success to self, failure to others|
| Halo Effect                   | One positive trait colors overall impression  |
| Horn Effect                   | One negative trait colors overall impression  |
| Stereotyping                  | Assuming group characteristics apply to individual|
| Recency Effect                | Recent events weighted more heavily           |

---

## 6. Self-Concept and Self-Disclosure

### 6.1 Self-Concept Components

| Component             | Description                                     |
|-----------------------|-------------------------------------------------|
| Self-image            | How you see yourself                            |
| Self-esteem           | How you evaluate yourself                       |
| Self-efficacy         | Belief in your ability to succeed               |
| Reflected appraisal   | Self-concept shaped by others' reactions        |
| Social comparison     | Evaluating self relative to others              |

### 6.2 The Johari Window

The Johari Window (Luft & Ingham, 1955) models self-awareness and mutual
understanding in relationships.

```
                Known to Self       Unknown to Self
              ┌───────────────────┬───────────────────┐
Known to      │                   │                   │
Others        │    OPEN /         │    BLIND          │
              │    ARENA          │    SPOT            │
              │                   │                   │
              ├───────────────────┼───────────────────┤
Unknown to    │                   │                   │
Others        │    HIDDEN /       │    UNKNOWN         │
              │    FACADE         │                   │
              │                   │                   │
              └───────────────────┴───────────────────┘
```

| Quadrant     | Description                                        | Growth Strategy              |
|--------------|----------------------------------------------------|------------------------------|
| Open/Arena   | Known to self and others                           | Expand through disclosure    |
| Blind Spot   | Known to others but not to self                    | Seek and accept feedback     |
| Hidden/Facade| Known to self but hidden from others               | Practice appropriate disclosure|
| Unknown      | Unknown to both self and others                    | New experiences, reflection  |

**Professional Application:** In healthy IT teams, the Open quadrant is large.
Team members share knowledge freely and give honest feedback, reducing blind
spots and hidden areas.

---

## 7. Cultural Communication Differences

### 7.1 High-Context vs Low-Context Cultures (Hall, 1976)

| Dimension            | High-Context                     | Low-Context                     |
|----------------------|----------------------------------|---------------------------------|
| Communication style  | Indirect, implicit               | Direct, explicit                |
| Meaning              | Embedded in context and relationships | Stated clearly in words     |
| Nonverbal importance | Very high                        | Lower                           |
| Agreements           | Relationship-based               | Contract-based                  |
| Conflict approach    | Preserve harmony, indirect       | Address directly                |
| Examples             | Japan, China, Arab nations, Korea| USA, Germany, Scandinavia       |

### 7.2 Hofstede's Cultural Dimensions (Applied to IT Teams)

| Dimension               | Impact on IT Communication                        |
|--------------------------|--------------------------------------------------|
| Power Distance           | Willingness to disagree with manager/lead        |
| Individualism/Collectivism| Solo vs team recognition; decision-making style |
| Uncertainty Avoidance    | Tolerance for ambiguity in agile processes       |
| Masculinity/Femininity   | Competitive vs collaborative team culture        |
| Long-term Orientation    | Focus on quick wins vs sustainable solutions     |

### 7.3 Strategies for Cross-Cultural IT Communication

| Strategy                         | Description                                |
|----------------------------------|--------------------------------------------|
| Avoid idioms and slang           | Not everyone shares the same expressions   |
| Confirm understanding            | Ask for paraphrasing, not just "yes"       |
| Be patient with silence          | Some cultures use silence for processing   |
| Respect time zone differences    | Rotate meeting times for global teams      |
| Use visual aids                  | Diagrams transcend language barriers       |
| Document decisions in writing    | Reduces misunderstanding across cultures   |

---

## 8. Conflict Management Styles

### 8.1 Thomas-Kilmann Conflict Mode Instrument

```
                          Assertiveness (concern for own goals)
                          Low                          High
                    ┌─────────────────┬─────────────────────┐
Cooperativeness     │                 │                     │
(concern for        │   AVOIDING      │   COMPETING         │
other's goals)      │                 │                     │
                    │                 │                     │
Low                 ├─────────────────┤                     │
                    │                 │                     │
                    │   COMPROMISING  │                     │
                    │   (center)      │                     │
                    │                 │                     │
High                ├─────────────────┼─────────────────────┤
                    │                 │                     │
                    │  ACCOMMODATING  │   COLLABORATING     │
                    │                 │                     │
                    └─────────────────┴─────────────────────┘
```

### 8.2 Style Comparison

| Style           | Approach               | When Appropriate                        | IT Example                          |
|-----------------|------------------------|-----------------------------------------|-------------------------------------|
| Competing       | Win-lose; assertive    | Emergencies, security decisions         | Enforcing a critical security patch |
| Collaborating   | Win-win; problem-solve | Complex issues needing buy-in           | Architecture design decisions       |
| Compromising    | Split the difference   | Time pressure, moderate importance      | Negotiating sprint scope            |
| Avoiding        | Withdraw; postpone     | Trivial issues, needs cooling off       | Ignoring a minor code style debate  |
| Accommodating   | Yield; agree           | Preserving relationship, low stakes     | Accepting a teammate's tool choice  |

### 8.3 Constructive Conflict Resolution Steps

1. **Describe the behavior** (not the person) — "When the deploy happened without review..."
2. **Express the impact** — "...it caused a production outage."
3. **State your needs** — "I need us to follow the review process."
4. **Listen to the other perspective** — Practice active listening.
5. **Collaborate on a solution** — "How can we make reviews faster so we don't skip them?"
6. **Follow up** — Check that the agreed solution is working.

---

## 9. Professional Communication in IT Teams

### 9.1 Communication Channels by Situation

| Situation                      | Recommended Channel              | Reason                         |
|--------------------------------|----------------------------------|--------------------------------|
| Production outage              | War room (voice + chat)          | Real-time collaboration needed |
| Code review feedback           | Pull request comments            | Contextual, documented         |
| Project status update          | Email or wiki                    | Asynchronous, archivable       |
| Quick question                 | Instant message (Slack/Teams)    | Low-friction, fast             |
| Sensitive feedback             | 1-on-1 meeting (private)        | Respectful, nuanced            |
| Architecture decision          | Design document + meeting        | Complex, needs discussion      |
| Daily coordination             | Standup meeting (brief)          | Efficient team sync            |

### 9.2 Giving Technical Feedback (SBI Model)

| Component      | Description                           | Example                              |
|----------------|---------------------------------------|--------------------------------------|
| **S**ituation  | When and where it happened            | "During yesterday's code review..."  |
| **B**ehavior   | Observable, specific behavior         | "...the variable names were single letters." |
| **I**mpact     | Effect on the team/project            | "This makes the code harder to maintain." |

### 9.3 Communication Anti-Patterns to Avoid

| Anti-Pattern              | Description                                  |
|---------------------------|----------------------------------------------|
| Reply-all storms          | Unnecessary group responses to emails        |
| Meeting without agenda    | Wasted time, unclear outcomes                |
| Jargon overload           | Excluding non-technical stakeholders         |
| Passive-aggressive chat   | Indirect hostility in team messaging         |
| Over-documenting          | Writing pages when a sentence suffices       |
| Under-documenting         | Tribal knowledge with no written record      |

---

## References

- Adler, R.B. & Proctor, R.F. — *Looking Out, Looking In*
- Hall, E.T. — *Beyond Culture*
- Barnlund, D.C. — *A Transactional Model of Communication*
- Thomas, K.W. & Kilmann, R.H. — *Thomas-Kilmann Conflict Mode Instrument*
- Luft, J. & Ingham, H. — *The Johari Window*
- Hofstede, G. — *Cultures and Organizations: Software of the Mind*

---

*FLLC Enterprise — Professional Development Division*
*Author: Preston Furulie | Portland Community College | Spring 2026*
