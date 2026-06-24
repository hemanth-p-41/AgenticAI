from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.response import Response
from app.models.interview import Interview
from collections import defaultdict


class AnalyticsService:
    def __init__(self, db: Session, user=None):
        self.db = db
        self.user = user

    def category_analytics(self) -> Dict[str, Any]:
        # categories to consider
        cats = ['DSA', 'OOP', 'DBMS', 'OS', 'AI_ML', 'PROJECTS', 'BEHAVIORAL']
        per_cat = defaultdict(list)
        # gather all evaluated responses for the user
        resps = self.db.query(Response).filter(Response.user_id == self.user.id, Response.evaluation != None).all()
        for r in resps:
            ev = r.evaluation or {}
            cat = ev.get('category', 'UNKNOWN')
            score = ev.get('score', 0)
            per_cat[cat].append(score)

        categories = {}
        for c in cats:
            vals = per_cat.get(c, [])
            categories[c] = (sum(vals) / len(vals)) if vals else 0.0

        # overall
        all_scores = [s for vals in per_cat.values() for s in vals]
        overall = (sum(all_scores) / len(all_scores)) if all_scores else 0.0

        # best/worst
        non_empty = {k: v for k, v in categories.items() if v > 0}
        best = max(non_empty.items(), key=lambda kv: kv[1])[0] if non_empty else None
        worst = min(non_empty.items(), key=lambda kv: kv[1])[0] if non_empty else None

        return {
            'overall_score': overall,
            'strongest_area': best,
            'weakest_area': worst,
            'categories': categories,
        }

    def trends(self, last_n: int = 5) -> Dict[str, Any]:
        # last N interviews for the user ordered by created_at
        interviews = (
            self.db.query(Interview).filter(Interview.user_id == self.user.id).order_by(Interview.created_at.desc()).limit(last_n).all()
        )
        history = []
        for intr in reversed(interviews):
            # compute average score for this interview
            resps = self.db.query(Response).filter(Response.interview_id == intr.id, Response.evaluation != None).all()
            scores = [r.evaluation.get('score', 0) for r in resps if r.evaluation]
            avg = (sum(scores) / len(scores)) if scores else 0.0
            history.append(avg)

        improvement = 0.0
        if history and len(history) >= 2 and history[0] > 0:
            improvement = ((history[-1] - history[0]) / history[0]) * 100.0

        return {'history': history, 'improvement': improvement}

    def weakness_detection(self) -> Dict[str, Any]:
        # find frequently weak categories and repeated weaknesses
        resps = self.db.query(Response).filter(Response.user_id == self.user.id, Response.evaluation != None).all()
        cat_counts = defaultdict(list)
        weakness_texts = []
        for r in resps:
            ev = r.evaluation or {}
            cat = ev.get('category', 'UNKNOWN')
            score = ev.get('score', 0)
            cat_counts[cat].append(score)
            weakness_texts.extend(ev.get('weaknesses', []))

        avg_by_cat = {k: (sum(v) / len(v)) if v else 0.0 for k, v in cat_counts.items()}
        sorted_cats = sorted(avg_by_cat.items(), key=lambda kv: kv[1])
        frequent_weak = sorted_cats[:3]

        # repeated weakness phrases
        from collections import Counter
        repeated = [w for w, c in Counter(weakness_texts).most_common(5)]

        return {'frequently_weak_categories': frequent_weak, 'repeated_weaknesses': repeated}
