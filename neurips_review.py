import textwrap


class PaperChecklistNeurIPS2024:
    about = textwrap.dedent(
        """NeurIPS Paper Checklist Guidelines
        The NeurIPS Paper Checklist is designed to encourage best practices for responsible machine learning research, addressing issues of reproducibility, transparency, research ethics, and societal impact. The checklist is included in the LateX style file. Do not remove the checklist: The papers not including the checklist will be desk rejected.

        All submissions must be in PDF format, and in a single PDF file include, in this order, (1) the submitted paper; (2) optional technical appendices that support the paper with additional proofs, derivations, or results; (3) the NeurIPS paper checklist. The checklist should therefore follow the submissions's references and the (optional) supplemental material.  The checklist does NOT count towards the page limit."""
    )

    answer_format = textwrap.dedent(
        """
        Please read the checklist guidelines carefully for information on how to answer these questions. For each question in the checklist:

        - You should answer yes, no, or n/a.
        - n/a means either that the question is Not Applicable for that particular paper or the relevant information is Not Available.
        - If you would like to explain your answer (e.g., explain why the answer is "no", or provide more detail reviewers), consider referencing the section(s) of the paper that provide support for your answer.
        - You can also optionally write a short (1–2 sentence) justification of your answer."""
    )

    more_info = textwrap.dedent(
        """The checklist answers are an integral part of your paper submission.} They are visible to the reviewers, area chairs, senior area chairs, and ethics reviewers. You will be asked to also include it (after eventual revisions) with the final version of your paper, and its final version will be published with the paper. The checklist answers are visible to the reviewers, area chairs, senior area chairs, and ethics reviewers.

        Reviewers will be asked to use the checklist as one of the factors in their evaluation. While "yes" is generally preferable to "no", it is perfectly acceptable to answer "no" provided a proper justification is given (e.g., "error bars are not reported because it would be too computationally expensive" or "we were unable to find the license for the dataset we used"). In general, answering "no" or "n/a" is not grounds for rejection. While the questions are phrased in a binary way, we acknowledge that the true answer is often more nuanced, so please just use your best judgement and write a justification to elaborate. All supporting evidence can appear either in the main paper or the supplemental material provided in the appendix. If you answer "yes" to a question, in the justification please point to the section(s) where related material for the question can be found.

        We provide guidance on how to answer each question below. You may additionally refer to the blog post from 2021 introducing the checklist to learn more about its motivation and how it was created."""
    )

    claims = textwrap.dedent(
        """**Claims:** Do the main claims made in the abstract and introduction accurately reflect the paper's contributions and scope? Claims in the paper should match theoretical and experimental results in terms of how much the results can be expected to generalize. The paper's contributions should be clearly stated in the abstract and introduction, along with any important assumptions and limitations. It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper. Enter yes, no, or an explanation if appropriate. Answers are visible to reviewers. Claims in the paper should match theoretical and experimental results in terms of how much the results can be expected to generalize.

        - The paper's contributions should be clearly stated in the abstract and introduction, along with any important assumptions and limitations. It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper."""
    )

    limitations = textwrap.dedent(
        """**Limitations:** The authors are encouraged to create a separate "Limitations" section in their paper. The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally).

        - The authors should reflect on how these assumptions might be violated in practice and what the implications would be.

        - The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated.

        - The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon.

        - We understand that authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection. It is worth keeping in mind that a worse outcome might be if reviewers discover limitations that aren't acknowledged in the paper. In general, we advise authors to use their best judgement and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations.

        The answer NA means that the paper has no limitation while the answer No means that the paper has limitations, but those are not discussed in the paper."""
    )

    theory_assumptions_proofs = textwrap.dedent(
        """**Theory, Assumptions and Proofs:** If you are including theoretical results, did you state the full set of assumptions of all theoretical results, and did you include complete proofs of all theoretical results? All assumptions should be clearly stated or referenced in the statement of any theorems. The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, authors are encouraged to provide a short proof sketch to provide intuition. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        - Did you state the full set of assumptions of all theoretical results? All assumptions should be clearly stated or referenced in the statement of any theorems.

        - Did you include complete proofs of all theoretical results? The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, authors are encouraged to provide a short proof sketch to provide intuition. You are encouraged to discuss the relationship between your results and related results in the literature.

        - Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material.

        - Theorems and Lemmas that the proof relies upon should be properly referenced."""
    )

    experimental_results_reproducibility = textwrap.dedent(
        """**Experimental Result Reproducibility:** If the contribution is a dataset or model, what steps did you take to make your results reproducible or verifiable? Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), release of a model checkpoint, or other means that are appropriate to your research. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        - While NeurIPS does not require releasing code, we do require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example...
            - If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm.

            - If the contribution is primailry a new model architecture, the paper should describe the architecture fully.

            - If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset).

            - We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results."""
    )

    open_access_to_data_code = textwrap.dedent(
        """**Open Access to Data and Code:** If you ran experiments, did you include the code, data, and instructions needed to reproduce the main experimental results (either in the supplemental material or as a URL)? Please see the NeurIPS code and data submission guidelines for more details. While we encourage release of code and data, we understand that this might not be possible, so no is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark). At submission time, to preserve anonymity, remember to release anonymized versions. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        - Did you include the code, data, and instructions needed to reproduce the main experimental results (either in the supplemental material or as a URL)?

        - The instructions should contain the exact command and environment needed to run to reproduce the results.

        - Please see the NeurIPS code and data submission guidelines for more details.

        - Main experimental results include your new method and baselines. You should try to capture as many of the minor experiments in the paper as possible. If a subset of experiments are reproducible, you should state which ones are.

        - While we encourage release of code and data, we understand that this might not be possible, so "no because the code is proprietary" is an acceptable answer.

        - At submission time, to preserve anonymity, remember to release anonymized versions."""
    )

    experimental_setting_details = textwrap.dedent(
        """**Experimental Setting/ Details:** If you ran experiments, did you specify all the training details (e.g., data splits, hyperparameters, how they were chosen)? The full details can be provided with the code, but the important details should be in the main paper, and information about how hyperparameters were selected should appear either in the paper or supplementary materials. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        - The full details can be provided with the code, in appendix or as a supplement, but the important details should be in the main paper.

        - The answer NA means that the paper does not include experiments.

        - The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them.

        - The full details can be provided either with the code, in appendix, or as supplemental material."""
    )

    experiment_statistical_significance = textwrap.dedent(
        """**Experiment Statistical Significance:** Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments?

        - The answer NA means that the paper does not include experiments.

        - The authors should answer "Yes" if the results are accompanied by error bars, confi338 dence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper.

        - The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions).

        - The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.)

        - The assumptions made should be given (e.g., Normally distributed errors).

        - It should be clear whether the error bar is the standard deviation or the standard error of the mean.

        - It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified.

        - For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g. negative error rates).

        - If error bars are reported in tables or plots, The authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text."""
    )

    experiments_compute_resource = textwrap.dedent(
        """**Experiments Compute Resource:** For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments?

        - The answer NA means that the paper does not include experiments.

        - The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage.

        - The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute. The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper)."""
    )

    code_of_ethics = textwrap.dedent(
        """**Code Of Ethics:** Have you read the NeurIPS Code of Ethics and ensured that your research conforms to it? Enter yes, no, or an explanation if appropriate. Answers are visible to reviewers.

        - If you have special circumstances that require some sort of deviation from the Code of Ethics, please explain it here. Please make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in your jurisdiction)."""
    )

    broader_impacts = textwrap.dedent(
        """**Broader Impacts:** If appropriate for the scope and focus of your paper, did you discuss potential negative societal impacts of your work? Please see the Paper Checklist Guidelines for detailed instructions and examples of points that you may choose to discuss. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        - Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations.

        - We expect many papers to be foundational research and not tied to particular applications, let alone deployments. However, if you see a direct path to any negative applications, you should point it out. For example, if you improve the quality of generative models, you might point out that your approach can be used to generate Deepfakes for disinformation. On the other hand, if you develop a generic algorithm for optimizing neural networks, you do not need to mention that this could enable people to train models that generate Deepfakes faster.

        - Consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology.

        - If there are negative societal impacts, you could also discuss any mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML)."""
    )

    safeguards = textwrap.dedent(
        """**Safeguards:** Do you have safeguards in place for responsible release of models with a high risk for misuse (e.g., pretrained language models)? Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images.

        We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort."""
    )
    licenses = textwrap.dedent(
        """**Licenses:** If you are using existing assets (e.g., code, data, models), did you cite the creators and respect the license and terms of use? Cite the original paper that produced the code package or dataset. If possible, include a URL. Be sure to check the original license and respect its conditions. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        - Cite the original paper that produced the code package or dataset.

        - Remember to state which version of the asset you're using.

        - If possible, include a URL.

        - State the name of the license (e.g., CC-BY 4.0) for each asset.

        - If you scraped data from a particular source (e.g., website), you should state the copyright and terms of service of that source.

        - If you are releasing assets, you should include a license, copyright information, and terms of use in the package. If you are using a popular dataset, please check paperswithcode.com/datasets, which has curated licenses for some datasets. You are also encouraged to use their licensing guide to help determine the license of a dataset.

        - If you are repackaging an existing dataset, you should state the original license as well as the one for the derived asset (if it has changed).

        - If you cannot find this information online, you are encouraged to reach out to the asset's creators."""
    )

    assets = textwrap.dedent(
        """**Assets:** If you are releasing new assets, did you document them and provide these details alongside the assets? Researchers should communicate the details of the dataset or the model as part of their submissions via structured templates. This includes details about training, license, limitations, etc. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        - The answer NA means that the paper does not release new assets.

        - Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc.

        - The paper should discuss whether and how consent was obtained from people whose asset is used.

        - At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file."""
    )

    crowdsourcing_and_research_with_human_subjects = textwrap.dedent(
        """**Crowdsourcing and Research with Human Subjects:** If you used crowdsourcing or conducted research with human subjects, did you include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)? Including this information in the supplemental material is fine, but if the main contribution of your paper involves human subjects, then we strongly encourage you to include as much detail as possible in the main paper. According to the NeurIPS Code of Ethics, you must pay workers involved in data collection, curation, or other labor at least the minimum wage in your country. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        -Did you include the full text of instructions given to participants and screenshots, if applicable? Including this information in the supplemental material is fine, but if the main contribution of your paper involves human subjects, then we strongly encourage you to include as much detail as possible in the main paper."""
    )

    irb_approvals = textwrap.dedent(
        """**IRB Approvals:** Did you describe any potential participant risks and obtain Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your institution), if applicable? Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper. For initial submissions, do not include any information that would break anonymity, such as the institution conducting the review. Enter yes, no, n/a, or an explanation if appropriate. Answers are visible to reviewers.

        - Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper. We recognize that the procedures for this may vary significant between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution. For initial submissions, do not include any information that would break anonymity, such as the institution conducting the review.

        - We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution.

        - For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review."""
    )


class ReviewerGuidelinesNeurIPS2024:
    """
    Below is a description of the questions you will be asked on the review form for each paper and some guidelines on what to consider when answering these questions. Feel free to use the NeurIPS paper checklist included in each paper as a tool when preparing your review (some submissions may have the checklist as part of the supplementary materials). Remember that answering “no” to some questions is typically not grounds for rejection. When writing your review, please keep in mind that after decisions have been made, reviews and meta-reviews of accepted papers and opted-in rejected papers will be made public.
    """

    summary = textwrap.dedent(
        """# Summary
        Briefly summarize the paper and its contributions. This is not the place to critique the paper; the authors should generally agree with a well-written summary."""
    )
    strengths_and_weaknesses = textwrap.dedent(
        """# Strengths and Weaknesses
        Please provide a thorough assessment of the strengths and weaknesses of the paper, touching on each of the following dimensions:
        a. Originality: Are the tasks or methods new? Is the work a novel combination of well-known techniques? (This can be valuable!) Is it clear how this work differs from previous contributions? Is related work adequately cited?
        b. Quality: Is the submission technically sound? Are claims well supported (e.g., by theoretical analysis or experimental results)? Are the methods used appropriate? Is this a complete piece of work or work in progress? Are the authors careful and honest about evaluating both the strengths and weaknesses of their work?
        c. Clarity: Is the submission clearly written? Is it well organized? (If not, please make constructive suggestions for improving its clarity.) Does it adequately inform the reader? (Note that a superbly written paper provides enough information for an expert reader to reproduce its results.)
        d. Significance: Are the results important? Are others (researchers or practitioners) likely to use the ideas or build on them? Does the submission address a difficult task in a better way than previous work? Does it advance the state of the art in a demonstrable way? Does it provide unique data, unique conclusions about existing data, or a unique theoretical or experimental approach?  # You can incorporate Markdown and Latex into your review.  See https://openreview.net/faq."""
    )

    questions = textwrap.dedent(
        """# Questions
        Please list up and carefully describe any questions and suggestions for the authors. Think of the things where a response from the author can change your opinion, clarify a confusion or address a limitation. This can be very important for a productive rebuttal and discussion phase with the authors."""
    )

    limitations = textwrap.dedent(
        """# Limitations
        Have the authors adequately addressed the limitations and potential negative societal impact of their work? If not, please include constructive suggestions for improvement.
        In general, authors should be rewarded rather than punished for being up front about the limitations of their work and any potential negative societal impact. You are encouraged to think through whether any critical points are missing and provide these as feedback for the authors."""
    )

    ethical_concerns = textwrap.dedent(
        """# Ethical Concerns
        If there are ethical issues with this paper, please flag the paper for an ethics review. For guidance on when this is appropriate, please review the NeurIPS ethics guidelines."""
    )

    soundness = textwrap.dedent(
        """# Soundness
        Please assign the paper a numerical rating on the following scale to indicate the soundness of the technical claims, experimental and research methodology and on whether the central claims of the paper are adequately supported with evidence.
        4 excellent
        3 good
        2 fair
        1 poor"""
    )

    presentation = textwrap.dedent(
        """# Presentation
        Please assign the paper a numerical rating on the following scale to indicate the quality of the presentation. This should take into account the writing style and clarity, as well as contextualization relative to prior work.
        - 4 excellent
        - 3 good
        - 2 fair
        - 1 poor"""
    )

    contribution = textwrap.dedent(
        """# Contribution
        Please assign the paper a numerical rating on the following scale to indicate the quality of the overall contribution this paper makes to the research area being studied. Are the questions being asked important? Does the paper bring a significant originality of ideas and/or execution? Are the results valuable to share with the broader NeurIPS community.
        - 4 excellent
        - 3 good
        - 2 fair
        - 1 poor"""
    )

    overall = textwrap.dedent(
        """# Overall Rating
        Please provide an "overall score" for this submission. Choices:
        - 10: Award quality: Technically flawless paper with groundbreaking impact on one or more areas of AI, with exceptionally strong evaluation, reproducibility, and resources, and no unaddressed ethical considerations.
        - 9: Very Strong Accept: Technically flawless paper with groundbreaking impact on at least one area of AI and excellent impact on multiple areas of AI, with flawless evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
        - 8: Strong Accept: Technically strong paper with, with novel ideas, excellent impact on at least one area of AI or high-to-excellent impact on multiple areas of AI, with excellent evaluation, resources, and reproducibility, and no unaddressed ethical considerations.
        - 7: Accept: Technically solid paper, with high impact on at least one sub-area of AI or moderate-to-high impact on more than one area of AI, with good-to-excellent evaluation, resources, reproducibility, and no unaddressed ethical considerations.
        - 6: Weak Accept: Technically solid, moderate-to-high impact paper, with no major concerns with respect to evaluation, resources, reproducibility, ethical considerations.
        - 5: Borderline accept: Technically solid paper where reasons to accept outweigh reasons to reject, e.g., limited evaluation. Please use sparingly.
        - 4: Borderline reject: Technically solid paper where reasons to reject, e.g., limited evaluation, outweigh reasons to accept, e.g., good evaluation. Please use sparingly.
        - 3: Reject: For instance, a paper with technical flaws, weak evaluation, inadequate reproducibility and incompletely addressed ethical considerations.
        - 2: Strong Reject: For instance, a paper with major technical flaws, and/or poor evaluation, limited impact, poor reproducibility and mostly unaddressed ethical considerations.
        - 1: Very Strong Reject: For instance, a paper with trivial results or unaddressed ethical considerations"""
    )
    confidence = textwrap.dedent(
        """# Confidence
        Please provide a "confidence score" for your assessment of this submission to indicate how confident you are in your evaluation.  Choices:
        - 5: You are absolutely certain about your assessment. You are very familiar with the related work and checked the math/other details carefully.
        - 4: You are confident in your assessment, but not absolutely certain. It is unlikely, but not impossible, that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work.
        - 3: You are fairly confident in your assessment. It is possible that you did not understand some parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
        - 2: You are willing to defend your assessment, but it is quite likely that you did not understand the central parts of the submission or that you are unfamiliar with some pieces of related work. Math/other details were not carefully checked.
        - 1: Your assessment is an educated guess. The submission is not in your area or the submission was difficult to understand. Math/other details were not carefully checked.
        - Code of conduct acknowledgement. While performing my duties as a reviewer (including writing reviews and participating in discussions), I have and will continue to abide by the NeurIPS code of conduct (NeurIPS Code Of Conduct)."""
    )

    best_practices = textwrap.dedent(
        """# Best Practices
        - Be thoughtful. The paper you are reviewing may have been written by a first year graduate student who is submitting to a conference for the first time and you don't want to crush their spirits.
        - Be fair. Do not let personal feelings affect your review.
        - Be useful. A good review is useful to all parties involved: authors, other reviewers and AC/SACs. Try to keep your feedback constructive when possible.
        - Be specific. Do not make vague statements in your review, as they are unfairly difficult for authors to address.
        - Be flexible. The authors may address some points you raised in your review during the discussion period. Make an effort to update your understanding of the paper when new information is presented, and revise your review to reflect this.
        - Be timely. Please respect the deadlines and respond promptly during the discussion.  If you cannot complete your review on time, please let the AC know as soon as possible.
        - If someone pressures you into providing a positive or negative review for a submission, please notify program chairs right away (pc2024@neurips.cc).
        - If you notice unethical or suspect behavior, please notify your AC right away."""
    )


class AreaChairGuidelinesNeurIPS2024:
    overview = textwrap.dedent(
        """As an area chair (AC), your job is to ensure that all the submissions you are assigned have high quality reviews and good discussions. You should become familiar with the technical contents of all your submissions and are responsible for making the initial acceptance decisions, with guidance from your senior area chair (SAC).

        Your task is to write a meta-review that explains your decision (accept, reject, borderline) to the authors. Your comments should augment the reviews, and explain how the reviews, author response, and discussion were used to arrive at your decision. Do not dismiss or ignore a review unless you have a good reason for doing so. If the reviewers cannot come to a consensus, you should read the paper carefully and write a detailed meta-review. You are expected to discuss such difficult cases with your SAC."""
    )

    writing_the_metareview = textwrap.dedent(
        """# Writing the Meta-Review
        - Don't focus too much on the scores. Instead, look carefully at the comments. Judge the quality of the review rather than taking note of the reviewer's confidence score; the latter may be more a measure of personality.
        - Indicate that you have read the author response, even if you just say "the rebuttal did not overcome the reviewer's objections."
        - If you use information that is not in the reviews (e.g., from corresponding with one of the reviewers after the rebuttal period), tell the authors (a) that you have done so and (b) what that information is.
        - If you find yourself wanting to overrule a unanimous opinion of the referees, the standards for your summary should be at the level of a full review. In these cases, it would probably be best to solicit an auxiliary review.
        - Please attempt to take a decisive stand on borderline papers. Other than papers where there is a genuine disagreement, much of our work will involve borderline papers where no one confidently expresses excitement, nor are any major problems identified. These are the tough decisions where we need your judgment!
        - Try to counter biases you perceive in the reviews. Unfashionable subjects should be treated fairly but often aren't, to the advantage of the papers on more mainstream approaches. To help the NeurIPS community move faster out of local minima, it is important to encourage risk and recognize that new approaches can't initially yield state-of-the-art competitive results. Nor are they always sold according to the recipes we are used to."""
    )

    best_practices = textwrap.dedent(
        """# Best Practices
        - Please respect deadlines and respond to emails as promptly as possible.
        - It is okay to be unavailable for part of the review process (e.g., on vacation for a few days), but if you will be unavailable for more than that—especially during important windows (e.g., discussion, decision-making)—you must let your SAC know as soon as you can.
        - If you notice a conflict of interest with a submission that is assigned to you, please contact your SAC immediately so that the paper can be reassigned.
        - Be professional and listen to the reviewers, but do not give in to undue influence. We expect you to be familiar with all the papers that are assigned to you and to be able to argue about their technical content and contributions. Your responsibility is to make good decisions, not just facilitate reviewer discussions.
        - Be kind. It is important to acknowledge that personal situations, in particular during this year of a global pandemic, may lead to late or unfinished work among reviewers. In the event that a reviewer is unable to complete their work on time, we encourage you to be considerate of the personal circumstances; you might have to pick up the slack in some cases. In all communications, exhibit empathy and understanding.
        - DO NOT talk to other ACs about submissions that are assigned to you; other ACs may have conflicts with these submissions. If you feel that it’s important to discuss one submission in the context of another, please email program-chairs@neurips.cc. In general, your primary point of contact for any discussions should be your SAC. Your SAC does not have any conflicts with any of the submissions that are assigned to you.
        - DO NOT talk to other SACs or ACs about your own submissions (i.e., submissions you are an author on) or submissions with which you have a conflict of interest.
        - If you notice unethical or suspect behavior involving either authors or reviewers, please notify your SAC and program chairs."""
    )
