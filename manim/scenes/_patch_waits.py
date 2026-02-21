"""
Patch scenes that are under 2 minutes by increasing wait times.
Increases each self.wait(X) by a fixed delta based on current value.
"""
import re, os, subprocess, glob

BASE = os.path.dirname(os.path.abspath(__file__))

# Files that need patching (under 2 min)
SHORT = [
    'algo_02_quicksort.py',
    'econ_05_game_theory.py',
    'la_04_dot_product.py',
    'la_05_cross_product.py',
    'la_09_shear.py',
    'la_10_projection.py',
    'la_12_span.py',
    'la_13_lin_indep.py',
    'la_14_basis.py',
    'la_15_change_of_basis.py',
    'la_17_svd.py',
    'la_18_null_space.py',
    'la_19_column_space.py',
    'la_20_row_reduction.py',
    'la_22_det_zero.py',
    'la_23_eigen_why.py',
    'phys_03_induction.py',
    'phys_04_maxwell.py',
]

def patch(text):
    """
    Increase all self.wait(X) by:
      X <= 0.5  -> +0.3
      0.5 < X <= 1.5 -> +0.8
      1.5 < X <= 2.5 -> +1.0
      2.5 < X <= 3.5 -> +1.0
      X > 3.5 -> +1.5
    """
    def replace_wait(m):
        val = float(m.group(1))
        if val <= 0.5:
            new_val = val + 0.3
        elif val <= 1.5:
            new_val = val + 0.8
        elif val <= 2.5:
            new_val = val + 1.0
        elif val <= 3.5:
            new_val = val + 1.0
        else:
            new_val = val + 1.5
        # Format nicely
        if new_val == int(new_val):
            return f'self.wait({int(new_val)}.0)'
        else:
            return f'self.wait({new_val:.1f})'
    return re.sub(r'self\.wait\((\d+(?:\.\d+)?)\)', replace_wait, text)

for fname in SHORT:
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        print(f'SKIP (not found): {fname}')
        continue
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()
    patched = patch(original)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(patched)
    # count wait additions
    orig_waits = [float(m) for m in re.findall(r'self\.wait\((\d+(?:\.\d+)?)\)', original)]
    new_waits  = [float(m) for m in re.findall(r'self\.wait\((\d+(?:\.\d+)?)\)', patched)]
    added = sum(new_waits) - sum(orig_waits)
    print(f'{fname}: +{added:.1f}s wait time added ({len(orig_waits)} wait calls)')

print('\nPatch complete.')
