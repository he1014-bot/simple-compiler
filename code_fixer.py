#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code Fixer Module
Function: Detect and fix common errors in source code, generate error reports and fixed code
"""

import re
from typing import List, Dict, Tuple

class CodeFixer:
    """Code fixer for common compiler errors"""
    
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.lines = source_code.split('\n')
        self.fixes_applied = []
        self.fixed_code = source_code
        self.error_report = []
    
    def detect_and_fix_errors(self) -> Tuple[str, List[str], List[str]]:
        """Detect and fix common errors in source code"""
        self.fixed_code = self.source_code
        self.fixes_applied = []
        self.error_report = []
        
        # Apply various fixers in a logical order
        # 1. First fix keyword typos (they affect other fixes)
        self._fix_typo_keywords()
        
        # 2. Fix variable declaration issues
        self._fix_variable_declaration()
        
        # 3. Fix missing parentheses (affects statement detection)
        self._fix_missing_parentheses()
        
        # 4. Fix for loop errors
        self._fix_for_loop_errors()
        
        # 5. Fix missing semicolons
        self._fix_missing_semicolons()
        
        # 6. Fix missing braces (should be last as it adds new lines)
        self._fix_missing_braces()
        
        # 7. Additional generic fixes
        self._fix_common_patterns()
        
        # Generate error report
        self._generate_error_report()
        
        return self.fixed_code, self.fixes_applied, self.error_report
    
    def _fix_missing_semicolons(self):
        """Fix missing semicolons at end of statements"""
        lines = self.fixed_code.split('\n')
        fixed_lines = []
        changes_made = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Skip empty lines and lines ending with {
            if not stripped or stripped.endswith('{'):
                fixed_lines.append(line)
                continue
            
            # Check for assignment without semicolon
            if re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^;{]+$', stripped):
                # Add semicolon
                fixed_lines.append(line.rstrip() + ';')
                changes_made = True
                self.fixes_applied.append(f"Added missing semicolon at line {i+1}")
            # Check for declaration without semicolon (with or without initialization, single or multiple variables)
            elif re.match(r'^\s*int\s+[a-zA-Z_][a-zA-Z0-9_]*(\s*=\s*[^;]+)?(\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*(\s*=\s*[^;]+)?)*\s*$', stripped):
                # Add semicolon
                fixed_lines.append(line.rstrip() + ';')
                changes_made = True
                self.fixes_applied.append(f"Added missing semicolon to declaration at line {i+1}")
            else:
                fixed_lines.append(line)
        
        if changes_made:
            self.fixed_code = '\n'.join(fixed_lines)
    
    def _fix_missing_braces(self):
        """Fix missing braces in compound statements"""
        lines = self.fixed_code.split('\n')
        fixed_lines = []
        changes_made = False
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for if/while/for without opening brace
            if re.match(r'^(if|while|for)\s*\(', line) and '{' not in line:
                # Look for statement on same line
                if ';' in line:
                    # Simple statement, need to add braces
                    parts = line.split(';', 1)
                    fixed_line = parts[0] + ' {'
                    fixed_lines.append(fixed_line)
                    fixed_lines.append('    ' + parts[1].strip() + ';')
                    fixed_lines.append('}')
                    changes_made = True
                    self.fixes_applied.append(f"Added braces for {line.split('(')[0]} statement at line {i+1}")
                else:
                    # Check next line
                    fixed_lines.append(lines[i])
            else:
                fixed_lines.append(lines[i])
            i += 1
        
        if changes_made:
            self.fixed_code = '\n'.join(fixed_lines)
    
    def _fix_missing_parentheses(self):
        """Fix missing parentheses in expressions"""
        lines = self.fixed_code.split('\n')
        fixed_lines = []
        changes_made = False
        
        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Check for if/while/for with missing closing parenthesis
            if re.match(r'^\s*(if|while|for)\s*\([^)]+$', stripped):
                # Look ahead for closing parenthesis
                found = False
                for j in range(i + 1, min(i + 3, len(lines))):  # Look up to 2 lines ahead
                    if ')' in lines[j]:
                        # Merge lines
                        merged = line.rstrip() + lines[j].lstrip()
                        fixed_lines.append(merged)
                        # Skip the line that was merged
                        i = j + 1
                        found = True
                        changes_made = True
                        self.fixes_applied.append(f"Fixed missing parenthesis at line {i}")
                        break
                
                if not found:
                    # Add closing parenthesis
                    fixed_lines.append(line.rstrip() + ')')
                    changes_made = True
                    self.fixes_applied.append(f"Added missing parenthesis at line {i+1}")
                    i += 1
            else:
                fixed_lines.append(line)
                i += 1
        
        if changes_made:
            self.fixed_code = '\n'.join(fixed_lines)
    
    def _fix_typo_keywords(self):
        """Fix common keyword typos"""
        replacements = {
            r'\bmaim\b': 'main',
            r'\bitn\b': 'int',
            r'\biff\b': 'if',
            r'\bels\b': 'else',
            r'\bwhiel\b': 'while',
            r'\bfo\b': 'for',
        }
        
        for pattern, replacement in replacements.items():
            new_code = re.sub(pattern, replacement, self.fixed_code, flags=re.IGNORECASE)
            if new_code != self.fixed_code:
                self.fixed_code = new_code
                self.fixes_applied.append(f"Fixed keyword typo: {pattern} -> {replacement}")
    
    def _fix_variable_declaration(self):
        """Fix variable declaration issues"""
        lines = self.fixed_code.split('\n')
        fixed_lines = []
        changes_made = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check for variable declaration without type specifier
            # Pattern: variable names without type (e.g., "a, b;")
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*(\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*\s*;?$', stripped):
                # Check if it already has a type specifier
                if not re.search(r'\b(int|float|double|char)\b', stripped):
                    # Add 'int' type specifier
                    fixed_lines.append('int ' + stripped)
                    changes_made = True
                    self.fixes_applied.append(f"Added 'int' type specifier at line {i+1}")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        if changes_made:
            self.fixed_code = '\n'.join(fixed_lines)
    
    def _fix_for_loop_errors(self):
        """Fix common for loop errors (missing semicolons in for statement)"""
        lines = self.fixed_code.split('\n')
        fixed_lines = []
        changes_made = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check for for loop with missing semicolons
            # Pattern: for (init condition update)
            if re.match(r'^\s*for\s*\([^;)]+\s+[^;)]+\s+[^;)]+\)', stripped):
                # Try to add semicolons
                # Match the for loop pattern
                match = re.match(r'^\s*(for\s*\([^;)]+)\s+([^;)]+)\s+([^;)]+)\)', stripped)
                if match:
                    init = match.group(1)
                    condition = match.group(2)
                    update = match.group(3)
                    fixed_line = f"{init}; {condition}; {update})"
                    fixed_lines.append(fixed_line)
                    changes_made = True
                    self.fixes_applied.append(f"Fixed for loop missing semicolons at line {i+1}")
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        if changes_made:
            self.fixed_code = '\n'.join(fixed_lines)
    
    def _fix_common_patterns(self):
        """Fix other common error patterns"""
        lines = self.fixed_code.split('\n')
        fixed_lines = []
        changes_made = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Fix missing commas in variable declarations
            # Pattern: int a b c;
            if re.match(r'^\s*int\s+[a-zA-Z_][a-zA-Z0-9_]+\s+[a-zA-Z_][a-zA-Z0-9_]', stripped):
                # Add commas between variable names
                parts = stripped.split()
                if len(parts) >= 3 and parts[0] == 'int':
                    # Reconstruct with commas
                    fixed_line = f"{parts[0]} {parts[1]}"
                    for part in parts[2:]:
                        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', part):
                            fixed_line += f", {part}"
                        else:
                            fixed_line += f" {part}"
                    fixed_lines.append(fixed_line)
                    changes_made = True
                    self.fixes_applied.append(f"Added missing commas in variable declaration at line {i+1}")
                else:
                    fixed_lines.append(line)
            
            # Fix missing operators in expressions
            # Pattern: a b (should be a + b or a = b, etc.)
            elif re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s+[a-zA-Z_][a-zA-Z0-9_]*\s*[;=]', stripped):
                # This is complex, skip for now
                fixed_lines.append(line)
            
            else:
                fixed_lines.append(line)
        
        if changes_made:
            self.fixed_code = '\n'.join(fixed_lines)
    
    def _generate_error_report(self):
        """Generate error report based on fixes applied"""
        if not self.fixes_applied:
            self.error_report.append("No errors detected in source code.")
            return
        
        self.error_report.append("ERROR REPORT")
        self.error_report.append("=" * 60)
        self.error_report.append(f"Original code had {len(self.fixes_applied)} issues that were fixed:")
        
        for i, fix in enumerate(self.fixes_applied, 1):
            self.error_report.append(f"{i}. {fix}")
        
        self.error_report.append("")
        self.error_report.append("FIXED CODE GENERATED")
        self.error_report.append("=" * 60)
    
    def save_fixed_code(self, filename: str):
        """Save fixed code to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.fixed_code)
        print(f"Fixed code saved to: {filename}")
    
    def save_error_report(self, filename: str):
        """Save error report to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            for line in self.error_report:
                f.write(line + '\n')
        print(f"Error report saved to: {filename}")
    
    def print_summary(self):
        """Print fix summary"""
        print("Code Fixer Summary:")
        print("=" * 60)
        if self.fixes_applied:
            print(f"Applied {len(self.fixes_applied)} fixes:")
            for fix in self.fixes_applied:
                print(f"  - {fix}")
        else:
            print("No fixes needed.")
        print("=" * 60)


def test_code_fixer():
    """Test code fixer with example code"""
    test_code = """maim(){
    itn a, b
    a = 10
    b = 20
    
    if (a > b
        a = b
    
    whiel (b > 0
        b = b - 1
}
"""
    
    print("Testing Code Fixer")
    print("=" * 60)
    print("Original Code:")
    print(test_code)
    print("=" * 60)
    
    fixer = CodeFixer(test_code)
    fixed_code, fixes, report = fixer.detect_and_fix_errors()
    
    print("Fixed Code:")
    print(fixed_code)
    print("=" * 60)
    
    fixer.print_summary()
    
    # Save results
    fixer.save_fixed_code("fixed_test.c")
    fixer.save_error_report("error_report.txt")
    
    print("\nError Report:")
    for line in report:
        print(line)


if __name__ == "__main__":
    test_code_fixer()
