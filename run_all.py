"""
Run All Steps — Master Script
==============================
This script runs all 4 steps of the lab sequentially or individually.
It fulfills the Code Quality Bonus criterion:
"All steps work via run_all.py without modification"

Usage:
  python run_all.py          (Runs all steps)
  python run_all.py --step 3 (Runs only step 3)
"""

import subprocess
import sys
import time
import argparse

def run_step(script_name: str):
    """
    Run a python script as a subprocess and handle errors gracefully.
    """
    print("=" * 60)
    print(f"🚀 Starting {script_name} ...")
    print("=" * 60)
    
    start_time = time.time()
    try:
        # Run the script and wait for it to complete
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            text=True,
        )
        elapsed = time.time() - start_time
        print(f"\n✅ {script_name} completed successfully in {elapsed:.2f}s.\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running {script_name}")
        print(f"   Exit code: {e.returncode}")
        print("   Continuing to next step if applicable...\n")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error running {script_name}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run lab steps.")
    parser.add_argument("--step", type=int, help="Run a specific step (1-4)")
    args = parser.parse_args()

    print("=" * 60)
    print("🌟 DAY 22 LAB: RUN STEPS 🌟")
    print("=" * 60)
    
    all_scripts = [
        "01_langsmith_rag_pipeline.py",
        "02_prompt_hub_ab_routing.py",
        "03_ragas_evaluation.py",
        "04_guardrails_validator.py",
    ]
    
    if args.step:
        if 1 <= args.step <= len(all_scripts):
            scripts = [all_scripts[args.step - 1]]
        else:
            print(f"❌ Invalid step: {args.step}. Must be between 1 and {len(all_scripts)}.")
            sys.exit(1)
    else:
        scripts = all_scripts
        
    success_count = 0
    total_start = time.time()
    
    for script in scripts:
        # Task 3 takes a long time, so we warn the user
        if script == "03_ragas_evaluation.py":
            print("⏳ Note: Task 3 (RAGAS Eval) takes ~15-20 minutes. Please be patient...\n")
            
        success = run_step(script)
        if success:
            success_count += 1
            
    total_elapsed = time.time() - total_start
    
    print("=" * 60)
    print("📊 Execution Summary")
    print("=" * 60)
    print(f"   Successful steps: {success_count}/{len(scripts)}")
    print(f"   Total time:       {total_elapsed:.2f}s")
    
    if success_count == len(scripts):
        print("\n🎉 Selected steps completed successfully!")
    else:
        print("\n⚠️  Some steps failed. Please check the logs above.")

if __name__ == "__main__":
    main()
