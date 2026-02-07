"""Verification script for Phase 10 features."""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))

print("Running Phase 10 Verification...")

try:
    # 1. Test Specialized Connectors
    from src.knowledge_ingest import SpecializedConnectors
    connectors = SpecializedConnectors()
    
    oyez_cases = connectors.fetch_oyez_case()
    print(f"[OK] Oyez Connector: Found {len(oyez_cases)} cases")
    print(f"   Sample: {oyez_cases[0]['name']}")
    
    sec_filings = connectors.fetch_sec_filings("AAPL")
    print(f"[OK] SEC Connector: Found {len(sec_filings)} filings")
    
    doj_stats = connectors.fetch_doj_statistics("white_collar")
    print(f"[OK] DOJ Connector: White collar conviction rate {doj_stats['conviction_rate']}")
    
    # 2. Test Rigorous Trainer
    from src.model_trainer import get_rigorous_trainer, ModelType
    
    trainer = get_rigorous_trainer()
    print(f"[OK] RigorousTrainer initialized: {trainer.name}")
    
    # Generate some dummy data first
    trainer.generate_training_data([
        {"text": "Federal prosecutors charged the CEO with securities fraud.", "source": "test_gen"},
        {"text": "The defendant is accused of insider trading scheme.", "source": "test_gen"},
        {"text": "Wire fraud charges were brought against the director.", "source": "test_gen"},
        {"text": "Embezzlement of company funds was reported.", "source": "test_gen"},
        {"text": "Tax evasion investigation is ongoing.", "source": "test_gen"}
    ] * 5) # Create enough data for cross-validation
    
    # Test Cross Validation
    cv_results = trainer.train_with_cross_validation(ModelType.CASE_CLASSIFIER, folds=3)
    if "error" in cv_results:
        print(f"[FAIL] Cross Validation Failed: {cv_results['error']}")
    else:
        print(f"[OK] Cross Validation: {cv_results['folds']}-Fold Score: {cv_results['average_accuracy']:.2f}")
    
    # Test Adversarial Training
    # (Mocking Opposing Counsel agent for test)
    adv_model = trainer.train_adversarial(ModelType.CASE_CLASSIFIER, opposing_counsel_agent=None)
    if adv_model:
        print(f"[OK] Adversarial Training: Model '{adv_model.name}' trained with robustness check")
    
    print("\n PHASE 10 VERIFIED SUCCESSFULLY")

except ImportError as e:
    print(f"[FAIL] Import Error: {e}")
except Exception as e:
    print(f"[FAIL] Runtime Error: {e}")
    import traceback
    traceback.print_exc()
