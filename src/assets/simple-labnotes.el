;;; ==============================================
;;; simple-labnotes.el --- edit local raw labnotes pages
;; Copyright (C) 2002, 2003  Alex Schroeder

;; Author: Alex Schroeder <alex@gnu.org>
;;         David Hansen <david.hansen@physik.fu-berlin.de>
;; Maintainer: David Hansen <david.hansen@physik.fu-berlin.de>
;; Version: 1.0.9
;; Keywords: hypermedia
;; URL: http://www.emacswiki.org/cgi-bin/wiki.pl?SimpleWikiEditMode

;; This file is not part of GNU Emacs.

;; This is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2, or (at your option)
;; any later version.

;; This is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with GNU Emacs; see the file COPYING.  If not, write to the
;; Free Software Foundation, Inc., 59 Temple Place - Suite 330,
;; Boston, MA 02111-1307, USA.
;; ==================================================
;;; Modified from simple-wiki.el, Gao Wang 2012
;;
;;; Commentary:

;; Use `simple-labnotes-mode' to edit raw labnotes pages.  This is useful for
;; temp files when editing textareas in w3m, for example.  Here is how
;; to do that:
;;
;; (add-to-list 'auto-mode-alist '("w3mtmp" . simple-labnotes-mode))

;;; Code:

(require 'font-lock)

(defvar simple-labnotes-version "1.0.9")

(defvar simple-labnotes-common-hook nil
  "Hook to run in every simple-labnotes mode.")



;; the default value are for the emacslabnotes

(defvar simple-labnotes-tag-list
  ;; xemacs requires an alist for `completing-read'.
  '(("u" . nil) ("b" . nil) ("i" . nil) ("strong" . nil) ("em" . nil)
    ("nolabnotes" . nil) ("code" . nil) ("tt" . nil) ("pre". t))
  "Alist of supported tags used for `completing-read'.
The cdr of a pair is non-nil if a newline should be inserted after the
opening tag.")

(if (featurep 'xemacs) ;; xemacs doesn't know character classes
    (defvar simple-labnotes-link-pattern
      ;; c&p from oddmuse sources, weird doesn't work perfectly so use
      ;; a different for gnu emacs
      '("\\<\\([A-Z]+[a-z\x80-\xff]+[A-Z][A-Za-z\x80-\xff]*\\)" . 0)
      "The pattern matching camel case links.
A Pair of the pattern and the matching subexpression.")
  (defvar simple-labnotes-link-pattern
    '("\\<\\([A-Z]+?[[:lower:][:nonascii:]]+?[A-Z][[:lower:][:upper:]]*\\)" . 0)
    "The pattern matching camel case links.
A Pair of the pattern and the matching subexpression."))

(defvar simple-labnotes-free-link-pattern
  '(" \\[\\([^\n]+?\\)\\] " . 1)
  "The Pattern matching free links.
A Pair of the pattern and the matching subexpression.")

(defvar simple-labnotes-em-patterns
  '(("\\(\\W\\|^\\)\"\\([^\"]\\|[^\"]\"\\)*\"" . 0)        ; ''emph''
    ("\\(\\W\\|^\\)\"\"\\([^\"]\\|[^\"]\"\\)*\"\"" . 0)      ; '''strong'''
    ("\\(\\W\\|^\\)\"\"\"\\([^\"]\\|[^\"]\"\\)*\"\"\"" . 0)) ; '''''strong emph'''''
  "List of regexps to match emphasized, strong and strong emphasized text.
Actually a list of pairs with the pattern and the number of the matching
subexpression.")

(defvar simple-labnotes-headline-patterns
  '(("^###\n#! \\([^\n!]+\\)\n###$" . 1)
    ("^###\n#\\([^\n!]+\\)\n###$" . 1)
    ("^#! \\([^\n!]+\\)$" . 1)
    ("^#!! \\([^\n!]+\\)$" . 1)
    )
  "List of regexps to match headlines.
Actually a list of pairs with the pattern and the number of the matching
subexpression.")

(defvar simple-labnotes-smilies-pattern
  (cons (concat
         "[ \t]\\("
         ":-?D\\|:-?)\\|;-?\)\\|:-?]\\|8-\)\\|"
         ":-\\\\|\\|:-?[/\\\\]\\|:-?(\\|:-?{\\)"
         "\\W") 1)
  "Pair of the pattern used to match smilies an the matching subexpression.")

(defvar simple-labnotes-outline-patterns
  '("=+" . "=+[ \t]*\n")
  "Pair of patterns for `outline-regexp' and `outline-heading-end-regexp'.")

(defvar simple-labnotes-horiz-line-pattern
  '("-----*" . 0)
  "Pair of the pattern use to match a horizontal line and the subexpression.")

(defvar simple-labnotes-line-break-pattern
  'none
  "Pair of the pattern used to match a line break and matching subexpression.")

(defvar simple-labnotes-enum-pattern
  '("^\\([*#]*#+\\)\\([^#*]\\|$\\)" . 1)
  "Pair of the pattern to match an entry of a numbered list the subexpression.")

(defvar simple-labnotes-bullet-pattern
  '("^\\([*#]*\\*+\\)\\([^*#]\\|$\\)" . 1)
  "Pair of the pattern to match an entry of a bullet list the subexpression.")

(defvar simple-labnotes-indent-pattern
  '("^:+" . 0)
  "Pair of the pattern to match indented text and the matching subexpression.")

(defvar simple-labnotes-definition-pattern
  '("^\\(;+.*?:\\)" . 1)
  "Pair of the pattern to match definition lists and the subexpression.")

(defvar simple-labnotes-em-strings
  '("\"" . "\"")
  "Start and end string for emphasis text.")

(defvar simple-labnotes-strong-strings
  '("\"\"" . "\"\"")
  "Start and end strings for strong text.")

(defvar simple-labnotes-strong-em-strings
  '("\"\"\"" . "\"\"\"")
  "Start and end string for strong text.")

(defvar simple-labnotes-additional-keywords
  (list
   ;; time stamp at the beginning of the buffer
   '("\\`\\([0-9]+\\)[ \t]+\\(#.+?\\)\n"
     (1 font-lock-constant-face)
     (2 font-lock-warning-face))
   '("{\$\\([^\$]\\|[^\$]\$\\)*\$}" . font-lock-keyword-face) ; {$a .. b$}
   '("@@[^ \t@][^@]*[^ \t@]@@" . font-lock-string-face) ; @@a .. b@@
   '(simple-labnotes-match-tag-i . (0 'simple-labnotes-italic-face append))
   '(simple-labnotes-match-tag-b . (0 'simple-labnotes-bold-face append))
   '(simple-labnotes-match-tag-u . (0 'simple-labnotes-underline-face append))
   '(simple-labnotes-match-tag-tt . (0 'simple-labnotes-teletype-face append))
   '(simple-labnotes-match-tag-em . (0 'simple-labnotes-emph-face append))
   '(simple-labnotes-match-tag-strong . (0 'simple-labnotes-strong-face append))

   ;; tags FIXME: oddmuse knows no parameters
   (list (concat "\\(</?\\)"
                 "\\([A-Za-z]+\\)"
                 "\\(\\([ \t]+[a-zA-Z]+\\)=\\(\".*\"\\)\\)*"
                 "\\(/?>\\)?")
         '(1 'default t t)
         '(2 'font-lock-function-name-face t t)
         '(4 'font-lock-variable-name-face t t)
         '(5 'font-lock-string-face t t)
         '(6 'default t t))

   '(simple-labnotes-match-tag-nolabnotes . (0 'simple-labnotes-nolabnotes-face t))

   ;; code blocks
   '(simple-labnotes-match-tag-code . (0 'simple-labnotes-code-face t))
   '(simple-labnotes-match-tag-pre . (0 'simple-labnotes-code-face t))

   '(simple-labnotes-match-code-block . (0 'simple-labnotes-code-face t)))

  "Additional keywords for font locking.")

(defvar simple-labnotes-font-lock-keywords nil
  "Font lock keywords for simple labnotes mode.")

(defvar simple-labnotes-tag-history nil
  "History for `completing-read' of tags.")



;; custom groups

(defgroup simple-labnotes ()
  "Edit raw labnotes pages.")

(defgroup simple-labnotes-faces ()
  "Faces simple-labnotes-mode." :group 'simple-labnotes)



;; faces

;; xemacs doesn't know about :inherit.  Just set all heading to bold.
(if (featurep 'xemacs)
    (progn
      (defface simple-labnotes-heading-1-face
        '((t (:bold t)))
        "Face for Labnotes headings at level 1."
        :group 'simple-labnotes-faces)

      (defface simple-labnotes-heading-2-face
        '((t (:bold t)))
        "Face for Labnotes headings at level 2."
        :group 'simple-labnotes-faces)

      (defface simple-labnotes-heading-3-face
        '((t (:bold t)))
        "Face for Labnotes headings at level 3."
        :group 'simple-labnotes-faces)

      (defface simple-labnotes-heading-4-face
        '((t (:bold t)))
        "Face for Labnotes headings at level 4."
        :group 'simple-labnotes-faces)

      (defface simple-labnotes-heading-5-face
        '((t (:bold t)))
        "Face for Labnotes headings at level 5."
        :group 'simple-labnotes-faces)

      (defface simple-labnotes-heading-6-face
        '((t (:bold t)))
        "Face for Labnotes headings at level 6."
        :group 'simple-labnotes-faces))

  (defface simple-labnotes-heading-1-face
    '((((type tty pc) (class color)) (:foreground "yellow" :weight bold))
      (t (:height 1.2 :inherit simple-labnotes-heading-2-face)))
    "Face for Labnotes headings at level 1."
    :group 'simple-labnotes-faces)

  (defface simple-labnotes-heading-2-face
    '((((type tty pc) (class color)) (:foreground "lightblue" :weight bold))
      (t (:height 1.2 :inherit simple-labnotes-heading-3-face)))
    "Face for Labnotes headings at level 2."
    :group 'simple-labnotes-faces)

  (defface simple-labnotes-heading-3-face
    '((((type tty pc) (class color)) (:weight bold))
      (t (:height 1.2 :inherit simple-labnotes-heading-4-face)))
    "Face for Labnotes headings at level 3."
    :group 'simple-labnotes-faces)

  (defface simple-labnotes-heading-4-face
    '((((type tty pc) (class color)) (:weight bold))
      (t (:weight bold :inherit variable-pitch)))
    "Face for Labnotes headings at level 4."
    :group 'simple-labnotes-faces)

  (defface simple-labnotes-heading-5-face
    '((((type tty pc) (class color)) (:weight bold))
      (t (:weight bold :inherit variable-pitch)))
    "Face for Labnotes headings at level 5."
    :group 'simple-labnotes-faces)

  (defface simple-labnotes-heading-6-face
    '((((type tty pc) (class color)) (:weight bold))
      (t (:weight bold :inherit variable-pitch)))
    "Face for Labnotes headings at level 6."
    :group 'simple-labnotes-faces))

(defface simple-labnotes-emph-face
  '((t (:italic t)))
  "Face for ''emphasis''."
  :group 'simple-labnotes-faces)

(defface simple-labnotes-strong-face
  '((t (:bold t)))
  "Face for '''strong emphasis'''."
  :group 'simple-labnotes-faces)

(defface simple-labnotes-strong-emph-face
  '((t (:bold t :italic t)))
  "Face for '''''stronger emphasis'''''."
  :group 'simple-labnotes-faces)

(defface simple-labnotes-italic-face
  '((t (:italic t)))
  "Face for <i>italic</i>."
  :group 'simple-labnotes-faces)

(defface simple-labnotes-bold-face
  '((t (:bold t)))
  "Face for <b>bold</b>."
  :group 'simple-labnotes-faces)

(if (featurep 'xemacs)
    (defface simple-labnotes-strike-face
      '((t (:strikethru t)))
      "Face for <strike>strike</strike>."
      :group 'simple-labnotes-faces)
  (defface simple-labnotes-strike-face
    '((t (:strike-through t)))
    "Face for <strike>strike</strike>."
    :group 'simple-labnotes-faces))

(defface simple-labnotes-underline-face
  '((t (:underline t)))
  "Face for <u>underline</u>."
  :group 'simple-labnotes-faces)

(defface simple-labnotes-local-link-face
  '((((class color) (background dark))
     (:foreground "skyblue3" :bold t))
    (((class color) (background light))
     (:foreground "royal blue" :bold t)))
  "Face for links to pages on the same labnotes."
  :group 'simple-labnotes-faces)

(defface simple-labnotes-teletype-face
  '((((class color) (background dark)) (:background "grey15"))
    (((class color) (background light)) (:background "moccasin")))
  "Face for <tt>teletype</tt>."
  :group 'simple-labnotes-faces)

(defface simple-labnotes-code-face
  '((((class color) (background dark)) (:background "grey15"))
    (((class color) (background light)) (:background "moccasin")))
  "Face for code in Labnotes pages."
  :group 'simple-labnotes-faces)

(defface simple-labnotes-nolabnotes-face
  '((((class color) (background dark))
     (:foreground "LightGoldenRod2"))
    (((class color) (background light))
     (:foreground "DarkGoldenRod2")))
  "Face for links to pages on the same labnotes."
  :group 'simple-labnotes-faces)

(defface simple-labnotes-smiley-face
  '((((class color) (background dark))
     (:foreground "gold" :bold t))
    (((class color) (background light))
     (:foreground "goldenrod" :bold t)))
  "Face for links to pages on the same labnotes."
  :group 'simple-labnotes-faces)



;; font lock matcher

(defun simple-labnotes-match-tag (tag limit)
  "Font lock matcher for regions within <TAG></TAG>."
  (when (search-forward (concat "<" tag ">") limit t)
    (let ((beg (match-end 0)) end)
      (if (search-forward (concat "</" tag ">") limit t)
          (setq end (match-beginning 0))
        (setq end (point)))
      (store-match-data (list beg end))
      t)))

(dolist (tag '("i" "b" "u" "tt" "nolabnotes" "code" "pre" "em"
               "strong" "math" "strike" "verbatim"))
  (eval `(defun ,(intern (concat "simple-labnotes-match-tag-" tag)) (limit)
           (simple-labnotes-match-tag ,tag limit))))

(defun simple-labnotes-end-of-code-block ()
  "Return the end of a code block if the cursor is within a code block.
Return nil otherwise."
  ;; FIXME: we assume that the line before code is empty.
  ;; this is not necessary in all cases.  known issues:
  ;;        (a) code starts directly after a heading.
  (save-excursion
    (backward-paragraph)
    (when (string-match "^$" (buffer-substring (point-at-bol) (point-at-eol)))
      (forward-line 1))
    (let ((char (char-after (point))))
      (when (and char (or (= char ?\t) (= char ? )))
        (forward-paragraph)
        (point)))))

(defun simple-labnotes-match-code-block (limit)
  (let (beg end)
    (when (re-search-forward "^[ \t]+[^ \t\n]" limit t)
      (setq beg (match-beginning 0))
      (setq end (simple-labnotes-end-of-code-block))
      (when end
        (if  (<= end beg)
            nil
          (store-match-data (list beg end))
          t)))))

(defun simple-labnotes-match-code-jsp (limit)
  "Match regions of preformated text in jsp labnotess."
  (when (search-forward "{{{" limit t)
    (let ((beg (match-end 0)) end)
      (if (search-forward "}}}" limit t)
          (setq end (match-beginning 0))
        (setq end (point)))
      (store-match-data (list beg end))
      t)))



;; editing functions

(defun simple-labnotes-strings-around-region (min max strmin strmax)
  "Insert the strings STRMIN and STRMAX at positions MIN and MAX."
  (save-excursion
    (goto-char min)
    (insert strmin)
    (goto-char (+ max (length strmin)))
    (insert strmax)))

(defun simple-labnotes-emph-region (min max)
  "Marke up text of the region emphasized."
  (interactive "r")
  (if (equal simple-labnotes-em-strings 'none)
      (error "No emphasis strings defined.")
    (simple-labnotes-strings-around-region
     min max
     (car simple-labnotes-em-strings)
     (cdr simple-labnotes-em-strings))))

(defun simple-labnotes-strong-region (min max)
  "Marke up text of the region strong."
  (interactive "r")
  (if (equal simple-labnotes-strong-strings 'none)
      (error "No strong strings defined.")
    (simple-labnotes-strings-around-region
     min max
     (car simple-labnotes-strong-strings)
     (cdr simple-labnotes-strong-strings))))

(defun simple-labnotes-strong-emph-region (min max)
  "Mark up text of the region strong emphasized."
  (interactive "r")
  (if (equal simple-labnotes-strong-em-strings 'none)
      (error "No strong emphasis strings defined.")
    (simple-labnotes-strings-around-region
     min max
     (car simple-labnotes-strong-em-strings)
     (cdr simple-labnotes-strong-em-strings))))

(defun simple-labnotes-insert-around-pos (before-str after-str)
  "Insert strings BEFORE-STR and AFTER-STR before and after the cursor."
  (insert before-str)
  (save-excursion (insert after-str)))

(defun simple-labnotes-insert-emph ()
  "Insert emphasized text."
  (interactive)
  (if (equal simple-labnotes-em-strings 'none)
      (error "No emphasis strings defined.")
    (simple-labnotes-insert-around-pos
     (car simple-labnotes-em-strings)
     (cdr simple-labnotes-em-strings))))

(defun simple-labnotes-insert-strong ()
  "Insert strong text."
  (interactive)
  (if (equal simple-labnotes-strong-strings 'none)
      (error "No strong strings defined.")
    (simple-labnotes-insert-around-pos
     (car simple-labnotes-strong-strings)
     (cdr simple-labnotes-strong-strings))))

(defun simple-labnotes-insert-strong-emph ()
  "Insert strong emphasized text."
  (interactive)
  (if (equal simple-labnotes-strong-em-strings 'none)
      (error "No strong emphasis strings defined.")
    (simple-labnotes-insert-around-pos
     (car simple-labnotes-strong-em-strings)
     (cdr simple-labnotes-strong-em-strings))))

(defun simple-labnotes-insert-tag-string (tag &optional closing)
  "Insert a the string \"<TAG>\" or \"</TAG>\" if CLOSING is non-nil."
  (when (and tag (not (string= tag "")))
    (if closing (insert "</") (insert "<"))
    (insert tag)
    (insert ">")))

(defun simple-labnotes-get-tag ()
  (let (prompt)
    (if (and simple-labnotes-tag-history (car simple-labnotes-tag-history))
        (setq prompt (concat "Tag (" (car simple-labnotes-tag-history) "): "))
      (setq prompt "Tag: "))
    (setq tag (completing-read prompt simple-labnotes-tag-list nil nil ""
                               'simple-labnotes-tag-history
                               (car simple-labnotes-tag-history))))
  (unless (assoc tag simple-labnotes-tag-list)
    (add-to-list 'simple-labnotes-tag-list (cons tag nil)))
  tag)

(defun simple-labnotes-tag-region (min max &optional tag)
  "Insert opening and closing text at begin and end of the region."
  (interactive "r")
  (unless tag
    (setq tag (simple-labnotes-get-tag)))
  (let ((taglen (+ 2 (length tag))))
    (save-excursion
      (goto-char min)
      (simple-labnotes-insert-tag-string tag)
      (when (and (assoc tag simple-labnotes-tag-list)
                 (cdr (assoc tag simple-labnotes-tag-list)))
        (setq taglen (1+ taglen))
        (insert "\n"))
      (goto-char (+ max taglen))
      (when (and (assoc tag simple-labnotes-tag-list)
                 (cdr (assoc tag simple-labnotes-tag-list)))
        (insert "\n"))
      (simple-labnotes-insert-tag-string tag t))))

(defun simple-labnotes-insert-tag (&optional tag)
  (interactive)
  "Insert a tag and put the cursor between the opening and closing tag."
  (unless tag
    (setq tag (simple-labnotes-get-tag)))
  (simple-labnotes-insert-tag-string tag)
  (save-excursion (simple-labnotes-insert-tag-string tag t))
  (when (and (assoc tag simple-labnotes-tag-list)
             (cdr (assoc tag simple-labnotes-tag-list)))
    (insert "\n")
    (save-excursion (insert "\n"))))

(if (featurep 'xemacs)
    (defun simple-labnotes-active-mark ()
      "Return non nil if the mark is active."
      (and zmacs-regions (mark)))
  (defun simple-labnotes-active-mark ()
    "Return non nil if the mark is active."
    (and transient-mark-mode mark-active)))

(defun simple-labnotes-insert-or-region-emph ()
  "Insert emphasized text.
If in `transient-mark-mode' and the region is active markup the region
emphasized."
  (interactive)
  (if (simple-labnotes-active-mark)
      (let ((beg (min (point) (mark))) (end (max (point) (mark))))
        (simple-labnotes-emph-region beg end))
    (simple-labnotes-insert-emph)))

(defun simple-labnotes-insert-or-region-strong ()
  "Insert strong text.
If in `transient-mark-mode' and the region is active markup the region
strong."
  (interactive)
  (if (simple-labnotes-active-mark)
      (let ((beg (min (point) (mark))) (end (max (point) (mark))))
        (simple-labnotes-strong-region beg end))
    (simple-labnotes-insert-strong)))

(defun simple-labnotes-insert-or-region-strong-emph ()
  "Insert strong emphasized text.
If in `transient-mark-mode' and the region is active markup the region
strong emphasized."
  (interactive)
  (if (simple-labnotes-active-mark)
      (let ((beg (min (point) (mark))) (end (max (point) (mark))))
        (simple-labnotes-strong-emph-region beg end))
    (simple-labnotes-insert-strong-emph)))

(defun simple-labnotes-insert-or-region-tag (&optional tag)
  "Insert opening and closing text around the cursor.
If in `transient-mark-mode' and the region is active put the tags around
the region."
  (interactive)
  (unless tag
    (setq tag (simple-labnotes-get-tag)))
  (if (simple-labnotes-active-mark)
      (let ((beg (min (point) (mark))) (end (max (point) (mark))))
        (simple-labnotes-tag-region beg end tag))
    (simple-labnotes-insert-tag tag)))



;; cursor movement

(defun simple-labnotes-next ()
  "Move the cursor to the beginning of the next link."
  (interactive)
  (let (pos1 pos2 (case-fold-search nil))
    (save-excursion
      (unless (equal simple-labnotes-link-pattern 'none)
        (when (re-search-forward (car simple-labnotes-link-pattern) nil t)
          (setq pos1 (match-beginning (cdr simple-labnotes-link-pattern))))))
    (save-excursion
      (unless (equal simple-labnotes-free-link-pattern 'none)
        (when (re-search-forward (car simple-labnotes-free-link-pattern) nil t)
          (setq pos2 (match-beginning (cdr simple-labnotes-free-link-pattern))))))
    (if (and pos1 pos2)
        (if (equal (min pos1 pos2) (point))
            (goto-char (max pos1 pos2))
          (goto-char (min pos1 pos2)))
      (if pos1
          (goto-char pos1)
        (if pos2
            (goto-char pos2))))))

(defun simple-labnotes-prev ()
  "Move the cursor to the beginning of the previous link"
  (interactive)
  (let (pos1 pos2 end-camelcase (case-fold-search nil))
    (save-excursion
      (unless (equal simple-labnotes-link-pattern 'none)
        (when (re-search-backward (car simple-labnotes-link-pattern) nil t)
          (setq pos1 (match-beginning (cdr simple-labnotes-link-pattern)))
          (setq end-camelcase (match-end (cdr simple-labnotes-link-pattern))))))
    (save-excursion
      (unless (equal simple-labnotes-free-link-pattern 'none)
        (when (re-search-backward (car simple-labnotes-free-link-pattern) nil t)
          (setq pos2 (match-beginning (cdr simple-labnotes-free-link-pattern))))))
    (if (and pos1 pos2)
        (if (and end-camelcase (equal (point) end-camelcase))
            (goto-char (min pos1 pos2))
          (goto-char (max pos1 pos2)))
      (if pos1
          (goto-char pos1)
        (if pos2
            (goto-char pos2))))))



;; mode definitions

(defun simple-labnotes-add-keyword (match-pair face overwrite)
  "Add an element to `simple-labnotes-font-lock-keywords'.
MATCH-PAIR has to be a pair with a regular expression and a
number for the subexpression: (REGEXP . NUMBER).  FACE is the
face used for highlighting and overwrite may be 'prepend,
'append, 'keep, t or nil.  See `font-lock-keywords'."
  (add-to-list
   'simple-labnotes-font-lock-keywords
   (cons (car match-pair) (list (cdr match-pair) `(quote ,face) overwrite))))

(defun simple-labnotes-add-font-lock-keywords ()
  "Add the default patterns to `simple-labnotes-font-lock-keywords'."

  ;; additional keywords
  (if (equal simple-labnotes-additional-keywords 'none)
      (setq simple-labnotes-font-lock-keywords nil)
    (setq simple-labnotes-font-lock-keywords simple-labnotes-additional-keywords))

  ;; local links
  (unless (equal simple-labnotes-link-pattern 'none)
    (simple-labnotes-add-keyword simple-labnotes-link-pattern
                             'simple-labnotes-local-link-face
                             'append))
  (unless (equal simple-labnotes-free-link-pattern 'none)
    (simple-labnotes-add-keyword simple-labnotes-free-link-pattern
                             'simple-labnotes-local-link-face
                             'append))
  ;; smilies
  (unless (equal simple-labnotes-smilies-pattern 'none)
    (simple-labnotes-add-keyword simple-labnotes-smilies-pattern
                             'simple-labnotes-smiley-face
                             t))
  ;; indent
  (unless (equal simple-labnotes-indent-pattern 'none)
    (simple-labnotes-add-keyword simple-labnotes-indent-pattern
                             'font-lock-comment-face
                             t))
  ;; horizontal lines
  (unless (equal simple-labnotes-horiz-line-pattern 'none)
    (simple-labnotes-add-keyword simple-labnotes-horiz-line-pattern
                             'font-lock-comment-face
                             t))
  ;; enums
  (unless (equal simple-labnotes-enum-pattern 'none)
    (simple-labnotes-add-keyword simple-labnotes-enum-pattern
                             'font-lock-constant-face
                             t))
  ;; bullet
  (unless (equal simple-labnotes-bullet-pattern 'none)
    (simple-labnotes-add-keyword simple-labnotes-bullet-pattern
                             'font-lock-keyword-face
                             t))
  ;;definition lists
  (unless (equal simple-labnotes-definition-pattern 'none)
    (simple-labnotes-add-keyword simple-labnotes-definition-pattern
                             'font-lock-type-face
                             t))
  ;; emphasis
  (let (em-re)
    (unless (equal simple-labnotes-em-patterns 'none)
      (when (setq em-re (first simple-labnotes-em-patterns))
        (simple-labnotes-add-keyword em-re 'simple-labnotes-emph-face 'append))
      (when (setq em-re (second simple-labnotes-em-patterns))
        (simple-labnotes-add-keyword em-re 'simple-labnotes-strong-face 'append))
      (when (setq em-re (third simple-labnotes-em-patterns))
        (simple-labnotes-add-keyword em-re
                                 'simple-labnotes-strong-emph-face
                                 'append))))
  ;; line breaks
  (unless (equal simple-labnotes-line-break-pattern 'none)
    (simple-labnotes-add-keyword simple-labnotes-line-break-pattern
                             'font-lock-warning-face
                             t))
  ;; head lines
  (let (head-re)
    (unless (equal simple-labnotes-headline-patterns 'none)
      (when (setq head-re (first simple-labnotes-headline-patterns))
        (simple-labnotes-add-keyword head-re 'simple-labnotes-heading-1-face t))
      (when (setq head-re (second simple-labnotes-headline-patterns))
        (simple-labnotes-add-keyword head-re 'simple-labnotes-heading-2-face t))
      (when (setq head-re (third simple-labnotes-headline-patterns))
        (simple-labnotes-add-keyword head-re 'simple-labnotes-heading-3-face t))
      (when (setq head-re (fourth simple-labnotes-headline-patterns))
        (simple-labnotes-add-keyword head-re 'simple-labnotes-heading-4-face t))
      ;; (when (setq head-re (fifth simple-labnotes-headline-patterns))
        ;; (simple-labnotes-add-keyword head-re 'simple-labnotes-heading-5-face t))
      ;; (when (setq head-re (sixth simple-labnotes-headline-patterns))
        ;; (simple-labnotes-add-keyword head-re 'simple-labnotes-heading-6-face t))
      )))

(defun simple-labnotes-define-major-mode (mode name doc-string &rest properties)
  "Define a major mode for editing a labnotes page.
MODE has to be a symbol which is used to build the major mode command:
e.g. 'emacslabnotes results in the command `simple-emacslabnotes-mode'. NAME
is a string which will appear in the status line (e.g. \"EmacsLabnotes\").
DOC-STRING is an an optional documentation string.  See
`definde-derived-mode'

To overwrite the default syntax (that should be fine for emacslabnotes or
any default oddmuse installation) you can specify various properties
as a list of keywords:

        :tags............... overwrite `simple-labnotes-tag-list'
        :camelcase.......... overwrite `simple-labnotes-link-pattern'
        :free-link.......... overwrite `simple-labnotes-free-link-pattern'
        :smilies............ overwrite `simple-labnotes-smilies-pattern'
        :em-strings......... overwrite `simple-labnotes-em-strings'
        :strong-strings..... overwrite `simple-labnotes-strong-strings'
        :strong-em-strings.. overwrite `simple-labnotes-strong-em-strings'
        :em-patterns........ overwrite `simple-labnotes-em-patterns'
        :headlines.......... overwrite `simple-labnotes-headline-patterns'
        :keywords........... overwrite `simple-labnotes-additional-keywords'
        :outline............ overwrite `simple-labnotes-outline-patterns'
        :linebreak.......... overwrite `simple-labnotes-line-break-pattern'
        :horiz.............. overwrite `simple-labnotes-horiz-line-pattern'
        :enum............... overwrite `simple-labnotes-enum-pattern'
        :bullet............. overwrite `simple-labnotes-bullet-pattern'
        :indent............. overwrite `simple-labnotes-indent-pattern'
        :deflist............ overwrite `simple-labnotes-definition-pattern'

Use the symbol 'none as the value if the labnotes doesn't support the property."
  (eval
   `(define-derived-mode
      ,(intern (concat "simple-" (symbol-name mode) "-mode"))
      text-mode ,name ,doc-string

      ;; ugly!  ugly!  ugly!
      (dolist (pair
               (list
                (cons 'simple-labnotes-tag-list
                      (quote ,(plist-get properties :tags)))
                (cons 'simple-labnotes-link-pattern
                      (quote ,(plist-get properties :camelcase)))
                (cons 'simple-labnotes-free-link-pattern
                      (quote ,(plist-get properties :free-link)))
                (cons 'simple-labnotes-smilies-pattern
                      (quote ,(plist-get properties :smilies)))
                (cons 'simple-labnotes-em-strings
                      (quote ,(plist-get properties :em-strings)))
                (cons 'simple-labnotes-strong-strings
                      (quote ,(plist-get properties :strong-strings)))
                (cons 'simple-labnotes-strong-em-strings
                      (quote ,(plist-get properties :strong-em-strings)))
                (cons 'simple-labnotes-em-patterns
                      (quote ,(plist-get properties :em-patterns)))
                (cons 'simple-labnotes-headline-patterns
                      (quote ,(plist-get properties :headlines)))
                (cons 'simple-labnotes-additional-keywords
                      (quote ,(plist-get properties :keywords)))
                (cons 'simple-labnotes-outline-patterns
                      (quote ,(plist-get properties :outline)))
                (cons 'simple-labnotes-line-break-pattern
                      (quote ,(plist-get properties :linebreak)))
                (cons 'simple-labnotes-horiz-line-pattern
                      (quote ,(plist-get properties :horiz)))
                (cons 'simple-labnotes-enum-pattern
                      (quote ,(plist-get properties :enum)))
                (cons 'simple-labnotes-bullet-pattern
                      (quote ,(plist-get properties :bullet)))
                (cons 'simple-labnotes-indent-pattern
                      (quote ,(plist-get properties :indent)))
                (cons 'simple-labnotes-definition-pattern
                      (quote ,(plist-get properties :deflist)))
                (cons 'simple-labnotes-outline-patterns
                      (quote ,(plist-get properties :outline)))))
        (when (cdr pair)
          (set (make-local-variable (car pair)) (cdr pair))))

      (unless (equal simple-labnotes-outline-patterns 'none)
        (setq outline-regexp (car simple-labnotes-outline-patterns))
        (setq outline-heading-end-regexp (cdr simple-labnotes-outline-patterns)))

      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-e" 'simple-labnotes-insert-or-region-emph)
      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-s" 'simple-labnotes-insert-or-region-strong)
      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-t" 'simple-labnotes-insert-or-region-tag)
      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-n" 'simple-labnotes-next)
      (define-key ,(intern (concat "simple-" (symbol-name mode) "-mode-map"))
        "\C-c\C-p" 'simple-labnotes-prev)

      (make-local-variable 'font-lock-defaults)
      (setq font-lock-multiline t)
      (simple-labnotes-add-font-lock-keywords)
      (setq font-lock-defaults  '(simple-labnotes-font-lock-keywords t))
      (goto-address)
      (font-lock-mode 1)
      (setq indent-tabs-mode nil)
      (run-hooks 'simple-labnotes-common-hook))))



;; mode definitions

;; oddmuse labnotess

;; for historical reasons define `simple-labnotes-mode'
(simple-labnotes-define-major-mode
 'labnotes
 "Labnotes"
 "Simple mode to edit labnotes pages.
\\{simple-labnotes-mode-map}")

(simple-labnotes-define-major-mode
 'emacslabnotes
 "EmacsLabnotes"
  "Simple mode to edit labnotes pages at http://www.emacslabnotes.org/.
\\{simple-emacslabnotes-mode-map}")

(simple-labnotes-define-major-mode
 'oddmuse
 "OddMuse"
 "Simple mode to edit labnotes pages at http://www.oddmuse.org/.
\\{simple-oddmuse-mode-map}"
 :camelcase 'none)



;; medialabnotes

(simple-labnotes-define-major-mode
 'medialabnotes
 "MediaLabnotes"
 "Simple mode to edit medialabnotes pages.
\\{simple-medialabnotes-mode-map}"
 :camelcase 'none

 :smilies 'none

 :linebreak '("<br>" . 0)

 :tags '(("b" . nil) ("big" . nil) ("blockquote" . nil) ("caption" . nil)
         ("code" . nil) ("center" . nil) ("cite" . nil) ("dfn" . nil)
         ("dl" . nil) ("em" . nil) ("i" . nil) ("kbd" . nil) ("math" . nil)
         ("nolabnotes" . nil) ("ol" . nil) ("pre" . nil) ("samp" . nil)
         ("small" . nil) ("strike" . nil) ("strong" . nil) ("sub" . nil)
         ("sup" . nil) ("tt" . nil) ("u" . nil) ("ul" . nil) ("var" . nil)
         ("a" . nil) ("div" . nil) ("font" . nil) ("table" . nil) ("td" . nil)
         ("tr" . nil))

 :keywords
 (list
  '(simple-labnotes-match-tag-i . (0 'simple-labnotes-italic-face append))
  '(simple-labnotes-match-tag-b . (0 'simple-labnotes-bold-face append))
  '(simple-labnotes-match-tag-u . (0 'simple-labnotes-underline-face append))
  '(simple-labnotes-match-tag-tt . (0 'simple-labnotes-teletype-face append))
  '(simple-labnotes-match-tag-em . (0 'simple-labnotes-emph-face append))
  '(simple-labnotes-match-tag-strong . (0 'simple-labnotes-strong-face append))
  '(simple-labnotes-match-tag-math . (0 'font-lock-string-face append))
  '(simple-labnotes-match-tag-strike . (0 'simple-labnotes-strike-face append))
  '(simple-labnotes-match-tag-code . (0 'simple-labnotes-code-face append))

  ;; tags
  (list (concat "\\(</?\\)"
                "\\([A-Za-z]+\\)"
                "\\(\\([ \t]+[a-zA-Z]+\\)=\\(\".*\"\\)\\)*"
                "\\(/?>\\)?")
        '(1 'default t t)
        '(2 'font-lock-function-name-face t t)
        '(4 'font-lock-variable-name-face t t)
        '(5 'font-lock-string-face t t)
        '(6 'default t t))

  ;; again.  otherwise overwritten by tag highlight.
  '("<br>" . (0 'font-lock-warning-face t))

  '(simple-labnotes-match-tag-nolabnotes . (0 'simple-labnotes-nolabnotes-face t))
  '(simple-labnotes-match-tag-pre . (0 'simple-labnotes-code-face t))

  '("^ .*$" . (0 'simple-labnotes-code-face t))))



;; phplabnotes

(simple-labnotes-define-major-mode
 'phplabnotes
 "PhpLabnotes"
 "Simple mode to edit php labnotes pages.
\\{simple-phplabnotes-mode-map}"

 :camelcase
 (if (featurep 'xemacs)
     ;; FIXME: no character classes.  only ascii chars will work.
     (cons (concat "\\([^~]\\|^\\)"
                   "\\<\\([A-Z][a-z]+"
                   "\\([A-Z][a-z]+\\)+\\)\\(\\>\\|'\\)")  2)
   (cons (concat "\\([^~]\\|^\\)"
                 "\\<\\([[:upper:]][[:lower:]]+"
                 "\\([[:upper:]][[:lower:]]+\\)+\\)\\(\\>\\|'\\)")  2))

 :free-link '("\\(^\\|[^~]\\)\\[\\([^\n]+?\\)\\]" . 2)

 :tags '(("pre" . t) ("verbatim" . t) ("b" . nil) ("big" . nil) ("i" . nil)
         ("small" . nil) ("tt" . nil) ("em" . nil) ("strong" . nil)
         ("abbr" . nil) ("acronym" . nil) ("cite" . nil) ("code" . nil)
         ("dfn" . nil) ("kbd" . nil) ("samp" . nil) ("var" . nil)
         ("sup" . nil) ("sub" . nil))

 :headlines '(("^[ \t]*!!!\\(.*?\\)$" . 1)
              ("^[ \t]*!!\\([^!].*?\\)$" . 1)
              ("^[ \t]*!\\([^!].*?\\)$" . 1)
              nil nil nil)

 :outline '("[ \t]*!+" . "\n")

 :em-strings '("_" . "_")

 :strong-strings '("*" . "*")

 :strong-em-strings '("_*" . "*_")

 ;; FIXME: this works not well with font-lock...
 :deflist '("^\\([^\n]+:\\)[ \t]*\n[ \t]+.*?" . 1)

 :em-patterns (list '("\\(\\W\\|^\\)_.*?_" . 0)
                    '("\\W\\*.*?\\*" . 0) ; bold at bol is a bullet list
                    (cons (concat "\\(\\(\\W\\|^\\)_\\*\\|\\W\\*_\\)"
                                  ".*?\\(\\_*\\|\\*_\\)")  0))

 :enum '("^\\([-*#o+ \t]*#+\\)\\([^-#*+]\\|$\\)" . 1)

 :bullet '("^\\([-*#o+ \t]*\\([-*+]\\|o[ \t]+\\)\\)\\([^-*#+]\\|$\\)" . 1)

 :smilies 'none

 :linebreak '("%%%" . 0)

 :indent 'none

 :keywords
 (list
  '(simple-labnotes-match-tag-i . (0 'simple-labnotes-italic-face append))
  '(simple-labnotes-match-tag-b . (0 'simple-labnotes-bold-face append))
  '(simple-labnotes-match-tag-tt . (0 'simple-labnotes-teletype-face append))
  '(simple-labnotes-match-tag-em . (0 'simple-labnotes-emph-face append))
  '(simple-labnotes-match-tag-strong . (0 'simple-labnotes-strong-face append))
  '(simple-labnotes-match-tag-code . (0 'simple-labnotes-code-face append))
  '(simple-labnotes-match-tag-pre . (0 'simple-labnotes-code-face append))

  '("\\(\\W\\|^\\)=.*?=" . (0 'simple-labnotes-teletype-face append))

  ;; tags FIXME: highlight plugins instead of parameters
  (list (concat "\\(</?\\)"
                "\\([A-Za-z]+\\)"
                "\\(\\([ \t]+[a-zA-Z]+\\)=\\(\".*\"\\)\\)*"
                "\\(/?>\\)?")
        '(1 'default t t)
        '(2 'font-lock-function-name-face t t)
        '(4 'font-lock-variable-name-face t t)
        '(5 'font-lock-string-face t t)
        '(6 'default t t))

  '(simple-labnotes-match-tag-verbatim . (0 'simple-labnotes-code-face t))))




;; jsplabnotes

(simple-labnotes-define-major-mode
 'jsplabnotes
 "JspLabnotes"
 "Simple mode to edit jsp labnotes pages.
\\{simple-jsplabnotes-mode-map}"

 ;; not the default but enabled on http://jsplabnotes.org
 :camelcase
 (if (featurep 'xemacs)
     ;; FIXME: no character classes.  only ascii chars will work.
     (cons (concat "\\([^~]\\|^\\)"
                   "\\(\\<[A-Z]+[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*\\>\\)") 2)
   (cons (concat "\\([^~]\\|^\\)"
                 "\\<\\([[:upper:]]+[[:lower:]][[:alnum:]]*"
                 "[[:upper:]][[:alnum:]]*\\>\\)") 2))

 :free-link '("\\(^\\|[^[]\\)\\[\\([^[][^\n]+?\\)\\]" . 2)

 ;; really?
 :tags 'none

 :headlines '(("^[ \t]*!!!\\(.*?\\)$" . 1)
              ("^[ \t]*!!\\([^!].*?\\)$" . 1)
              ("^[ \t]*!\\([^!].*?\\)$" . 1)
              nil nil nil)

 :outline '("[ \t]*!+" . "\n")

 :strong-strings '("__" . "__")

 :indent '("^;[ \t]*:" . 0)

 :deflist '("^\\(;+[ \t]*[^ \t]+?:\\)" . 1)

 :em-patterns (list '("\\(\\W\\|^\\)''.*?''" . 0)
                    '("\\(\\W\\|^\\)__.*?__" . 0)
                    (cons (concat "\\(\\W\\|^\\)\\(''__\\|__''\\)"
                                  ".*?\\(__''\\|''__\\)")  0))

 :linebreak '("\\\\\\\\" . 0)

 :keywords
 (list
  '("\\(\\W\\|^\\)\\({{[^{].*?}}\\)" .
    (2 'simple-labnotes-teletype-face append))
  '(simple-labnotes-match-code-jsp . (0 'simple-labnotes-code-face t))))



(provide 'simple-labnotes)

;;; simple-labnotes.el ends here
